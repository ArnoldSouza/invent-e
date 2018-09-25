import configparser  # lib to read config.ini files
import pyodbc  # module to establish SQL connection
import pandas as pd  # import lib to make a dataframe
from utils.time_stamp import timeit  # decorator to get elapsed time
from utils.animation import CursorAnimation  # animated waiting cursor
from utils.prompt import check_parameters, prompt_param, check_ini_file  # get input data from the user
from colorama import init, Fore  # colors to Windows Command Prompt

init(autoreset=True)  # start Windows Command Prompt


class DbConn:
    """
    Class to establish connection to the database server to
    retrieve information.
    Gets parameters from app_config.ini file and initiate the class.
    """

    def __init__(self, config_file, server_name):
        config = configparser.ConfigParser()
        config.read(config_file)  # get values from INI File

        self.server_name = check_ini_file(config_file, config, server_name, 'server')  # assign server name
        self.db_name = check_ini_file(config_file, config, server_name, 'database')  # assign db name
        self.user_name = check_ini_file(config_file, config, server_name, 'uid')  # assign user name
        self.pwd = check_ini_file(config_file, config, server_name, 'pwd')  # assign password
        self.conn = None

    # noinspection PyArgumentList
    def connect_db(self):
        """
        Method to establish connection to the server
        """
        try:
            print(Fore.YELLOW +
                  'Establishing connection with {}'.format(self.server_name))
            # timeout only of the connection, not of the SQL query
            self.conn = pyodbc.connect(Driver='SQL Server',
                                       Server=self.server_name,
                                       Database=self.db_name,
                                       uid=self.user_name,
                                       pwd=self.pwd,
                                       timeout=3)
            print(Fore.GREEN + 'Connection done!')
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '08001':
                print('Conn Error: Please check connection')
            elif sqlstate == '42000':
                print('Logon Error: Please check db_name')
            elif sqlstate == '28000':
                print('Logon Error: Please check user_name or password')
            elif sqlstate == 'HYT00':
                print('Time Error: Time Limit Exceed. Try again')
            else:
                print(ex.args)

    def close_db(self):
        """
        Close the connection to the database
        """
        self.conn.close()

    @staticmethod
    def read_sql_file(filename, dict_answers=None):
        """read a SQL Script file and pass it as a string
        :param filename: name of the SQL Script file
        :param dict_answers: dictionary of answers to put in the string, if given
        :return: SQL Script if parameters populated and the dict of parameters
        """
        if dict_answers is None:
            dict_answers = {}
        fd = open('SQL/' + filename + '.sql', 'r', encoding='utf-8')
        sql_file = fd.read()
        fd.close()
        sql_file, parameters = check_parameters(sql_file, dict_answers)
        return sql_file, parameters

    @timeit
    def sql_to_df(self, sql_file, action=False, dict_answers=None):
        """
        Gets data from the SQL server and return the result as a dataframe
        and a list of parameters, if exists
        """
        print(Fore.YELLOW + 'Fetching data from {}...'.format(self.db_name))
        if dict_answers is None:
            dict_answers = {}
        sql, parameters = self.read_sql_file(sql_file, dict_answers)
        animation = CursorAnimation()  # Load Cursor
        if action:
            animation.start()  # Start Animation
        # fetch data from server
        df = pd.read_sql(sql, self.conn)
        self.conn.commit()  # confirm or rollback changes made to the database
        if action:
            animation.stop()  # Stop Animation
        return df, parameters

    def sql_to_string(self, sql_file, action=False, print_msg=True):
        """
        Gets just one value from a table and return it as a string.
        It is used to fetch minimal information from de database.
        """
        if print_msg:
            print(Fore.YELLOW + 'Fetching data from {}...'.format(self.db_name))
        animation = CursorAnimation()  # Load Cursor
        if action is True:
            animation.start()  # Start Animation
        cur = self.conn.cursor()  # create cursor, required for connection
        cur.execute(sql_file)  # query db
        result = cur.fetchone()  # return one result
        self.conn.commit()  # confirm or rollback changes made to the database
        if action:
            animation.stop()  # Stop Animation
        if result is None:  # check if the result is null
            answer = None  # case yes, assign None
        else:
            answer = result[0]  # otherwise, assign the result
        return answer

    # TODO clear and adjust this function
    def get_complements(self, parameters, *args):
        """
        Sometimes the information presented in the dataframe is not enough to properly present it to the user.
        One example is when it's necessary to show both the SKU and the NAME of a product. So it's necessary to
        query the NAME given the SKU and return the NAME to use it. That's the intention of this method.
        :param parameters: Parameters to narrow the query of complements
        :param args: The info you want as a complement of information
        :return: String with the info
        """
        def properly_answer(key_string, given_answer, result_string, print_msg=True, message=None, assign_value=None):
            """
            Function to treat the result of a SQL query
            :param key_string: The parameter of to query
            :param given_answer: The dict that will be returned as answer
            :param result_string: The result of the past query
            :param print_msg: Whether to print or not the message
            :param message: Message to be printed
            :param assign_value: If result_string is None, the value to be assigned
            """
            flag = False
            if result_string is None:
                if assign_value:
                    flag = True
                    given_answer[arg] = assign_value
                else:
                    given_answer[arg] = 'Not Found'
            else:
                given_answer[arg] = result_string
            if print_msg:
                if flag:
                    print(message)
                else:
                    print(key_string, '->', given_answer[arg])
            return given_answer

        def get_info(dictionary, key):
            """
            Check if a key is in the parameters' dictionary. If not, prompt to user input this information
            :param dictionary: the parameters dict
            :param key: a specific key
            :return: the dictionary of parameters updated
            """
            if key not in dictionary:
                value = prompt_param(key)
                dictionary[key] = value
            else:
                value = dictionary[key]
            return value

        answer = {}
        for arg in args:
            if arg == 'product':
                sql_scrpt = f"""
                SELECT
                    RTRIM(SB1010.B1_COD)+' - '+RTRIM(SB1010.B1_DESC)
                FROM PROTHEUS.dbo.SB1010 SB1010
                WHERE
                    SB1010.D_E_L_E_T_<>'*' AND
                    SB1010.B1_COD = {get_info(parameters, 'codigo')}
                """
                answer = properly_answer(arg, answer, self.sql_to_string(sql_scrpt, print_msg=False))
            elif arg == 'warehouse':
                sql_scrpt = f"""
                SELECT
                    RTRIM(Z01010.Z01_CODGER)+' - '+RTRIM(Z01010.Z01_DESC)
                FROM PROTHEUS.dbo.Z01010 Z01010
                WHERE
                    Z01010.D_E_L_E_T_<>'*' AND
                    Z01010.Z01_FILIAL = {get_info(parameters, 'filial')} AND
                    Z01010.Z01_COD = {get_info(parameters, 'armazem')}
                """
                answer = properly_answer(arg, answer, self.sql_to_string(sql_scrpt, print_msg=False))
            elif arg == 'last_stock':
                sql_scrpt = f"""
                SELECT
                    SB2010.B2_QATU
                FROM PROTHEUS.dbo.SB2010 SB2010
                WHERE
                    SB2010.D_E_L_E_T_<>'*' AND
                    SB2010.B2_FILIAL = {get_info(parameters, 'filial')} AND
                    SB2010.B2_LOCAL = {get_info(parameters, 'armazem')} AND
                    SB2010.B2_COD = {get_info(parameters, 'codigo')}
                """
                answer = properly_answer(arg,
                                         answer,
                                         self.sql_to_string(sql_scrpt, print_msg=False),
                                         message='actual stock not found, assigning ZERO...',
                                         assign_value=0)
            else:
                msg = f"the argument '{arg}' is not set in this script. Please contact administrator to resolve it"
                raise ValueError(msg)
        return answer
