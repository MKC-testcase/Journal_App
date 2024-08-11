# importing the library to send queries to the database
import pyodbc
# importing re for data validation process before continuing to the database
import re
import configparser


class DB:
    def __init__(self, server_name, database, user_name, password):
        self._server_name = server_name
        self._database = database
        self._user_name = user_name
        self._password = password
        self._connection = None
        self._cursor = None


    # basics of operation
    def set_connection(self):
        """Sets up the connection to the database"""
        # basic connection string for the SQL Server Database
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self._server_name};\
        DATABASE={self._database};UID={self._user_name};PWD={self._password}'
        # creating the connection
        self.connection = pyodbc.connect(connection_string)
        self.create_cursor()

    def create_cursor(self):
        """Creates a cursor to interact with the database"""
        self.cursor = self.connection.cursor()

    def query_data(self, query):
        """Queries data from the database"""
        return self.cursor.execute(query).fetchall()
        
    def send_data(self, query):
        """Sends and commits data to the database"""
        try:
            self.cursor.execute(query)
            self.cursor.commit()
            return True
        except Exception:
            return False
    
    def end_connection(self):
        """ End the connection to the database """
        self.cursor.close()
        self.connection.close()

    # preventing users from being locked into 1 configuration
    def reset_credentials(self, server_name, database, user_name, password):
        """Allows the user to set the database to another database assuming given parameters"""
        try:
            # resetting the connection and the cursor
            self.connection.close()
            self.cursor = None
            print("Resetting Connection")
        except AttributeError:
            print("Resetting Connection")
        # creating new parameters for the database
        self._server_name = server_name
        self._database = database
        self._user_name = user_name
        self._password = password

    # query validation
    def query_validation(self, text_query, quotation_number):
        """Checks queries for basic SQL injection attacks, rejects queries when found"""
        # Remember to provide as little information as possible when rejecting queries, but log the real reason

        # checks the quotation number against the number of quotation marks in the query, reject if numbers mismatch
        # checks for the # sign in the query, reject 
        injector_regex = "[\"\']"
        comment_regex = "[#]"

        quotation_list = re.findall(injector_regex, text_query)
        if quotation_number != len(quotation_list):
            print(quotation_number, len(quotation_list))
            # log the injection attempt for too many quotation marks
            return False
        elif re.search(comment_regex, text_query):
            print("There has been a error with the query, try again")
            # log the injection attempt for altering the query via #
            return False
        else:
            return True
        
    