import configparser  # lib to read config.ini files
import pyodbc  # module to establish SQL connection
import pandas as pd  # import lib to make a dataframe
from Utils.time_stamp import timeit  # decorator to get elapsed time
from Utils.animation import CursorAnimation  # animated waiting cursor
from colorama import init, Fore  # colors to Windows Command Prompt
from Pretty.prompt import check_parameters  # get input data from the user

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

        self.server_name = config[server_name]['server']  # assign server name
        self.db_name = config[server_name]['database']  # assign db name
        self.user_name = config[server_name]['uid']  # assign user name
        self.pwd = config[server_name]['pwd']  # assign password
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
        :return: SQL Script if parameters populated
        """
        fd = open('SQL/' + filename + '.sql', 'r', encoding='utf-8')
        sql_file = fd.read()
        fd.close()
        sql_file = check_parameters(sql_file, dict_answers)
        return sql_file

    @timeit
    def sql_to_df(self, sql_file, action=False):
        """
        Gets data from the SQL server and return the result as a dataframe
        """
        print(Fore.YELLOW + 'Fetching data from {}...'.format(self.db_name))
        animation = CursorAnimation()  # Load Cursor
        if action:
            animation.start()  # Start Animation
        # fetch data from server
        df = pd.read_sql(self.read_sql_file(sql_file),
                         self.conn)
        self.conn.commit()  # confirm or rollback changes made to the database
        if action:
            animation.stop()  # Stop Animation
        return df

    @timeit
    def sql_to_string(self, sql_file, action=False):
        """
        Gets just one value from a table and return it as a string.
        It is used to fetch minimal information from de database.
        """
        print(Fore.YELLOW + 'Fetching data from {}...'.format(self.db_name))
        animation = CursorAnimation()  # Load Cursor
        if action is True:
            animation.start()  # Start Animation
        cur = self.conn.cursor()  # create cursor, required for connection
        cur.execute(self.read_sql_file(sql_file))  # query db
        result = cur.fetchone()  # return one result
        self.conn.commit()  # confirm or rollback changes made to the database
        if action:
            animation.stop()  # Stop Animation
        if result is None:  # check if the result is null
            answer = None  # case yes, assign None
        else:
            answer = result[0]  # otherwise, assign the result
        return answer
