import configparser  # lib to read config.ini files
import pyodbc  # module to establish SQL connection
import pandas as pd  # import lib to make a dataframe
from Utils.time_stamp import timeit  # decorator to get elapsed time
from Utils.animation import CursorAnimation  # animated waiting cursor
from colorama import init, Fore  # colors to Windows Command Prompt

init(autoreset=True)  # inicialize Windows Command Prompt


class db_conn:
    """
    Class to establish connection to the database server to
    retrieve information.
    Gets parameters from app_config.ini file and initiate the class.
    """

    def __init__(self, string_connection):
        config = configparser.ConfigParser()
        config.read('app_config.ini')  # get values from INI File
        self.server_name = config['ERP_SERVER']['server']  # assign server name
        self.db_name = config['ERP_SERVER']['database']  # assign db name
        self.user_name = config['ERP_SERVER']['uid']  # assign user name
        self.pwd = config['ERP_SERVER']['pwd']  # assign password

    def connect(self):
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

    def close(self):
        """
        Close the connection to the batabase
        """
        self.conn.close()

    @staticmethod
    def read_sql_file(filename):
        """read a SQL Script file and pass it as a string"""
        fd = open('SQL/' + filename + '.sql', 'r', encoding='utf-8')
        sqlFile = fd.read()
        fd.close()
        return sqlFile

    @timeit
    def sql_todf(self, sql_file, action=False):
        """
        Gets data from the SQL server and return the result as a dataframe
        """
        print(Fore.YELLOW + 'Fetching data from {}...'.format(self.db_name))
        if action is True:
            animation = CursorAnimation()  # Load Cursor
            animation.start()  # Start Animation
        # fetch data from server
        df = pd.read_sql(self.read_sql_file(sql_file),
                         self.conn)
        self.conn.commit()  # confirm or rollback changes made to the database
        if action:
            animation.stop()  # Stop Animation
        return df

    @timeit
    def sql_tostring(self, sql_file, action=False):
        """
        Gets just one value from a table and return it as a string.
        It is used to fetch minimal information from de database.
        """
        print(Fore.YELLOW + 'Fetching data from {}...'.format(self.db_name))
        if action is True:
            animation = CursorAnimation()  # Load Cursor
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
