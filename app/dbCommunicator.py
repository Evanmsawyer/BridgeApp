import mysql.connector
from mysql.connector import Error
import json
import os

class DBConnector:   
    """
    Class for connecting to a MySQL database

    example:
        db = DBConnector()
        result = db.execute_query("SELECT * FROM table")
        print(result) <-- this is a dict
    
    """
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        jsonconnectionpath = 'db_config.json'
        connectionpath = os.path.join(script_dir, jsonconnectionpath)
        self.db_config = self.load_db_config(connectionpath)
        self.connection = self.create_connection(self.db_config)
    
    #def __del__(self):
        #self.close_connection(self.connection)

    def load_db_config(self, filename):
        """
        Load database configuration from a JSON file

        Args:
            filename (str): The name of the JSON file containing the configuration

        Returns:
            dict: database configuration    
        """
        with open(filename, 'r') as file:
            return json.load(file)

    def create_connection(self, config):
        """
        creates DB connection

        Returns:
            connection: mysql.connector.connection_cext.CMySQLConnection object
        Raises:
            Error: If the connection cannot be established 
        """
        try:
            return mysql.connector.connect(**config)
        except Error as e:
            print(f"The error '{e}' occurred")

    def close_connection(self):
        """
        closes DB connection

        Args:
            connection (mysql.connector.connection_cext.CMySQLConnection): The connection to the database
        Raises:
            Error: If the connection cannot be closed 
        """
        try:
            self.connection.close()
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_query(self, query, parameters=(), fetchall=True, num_rows=0):
        """
        Executes DB query

        Args:
            query (str): The query to be executed
            parameters (tuple, optional): The parameters to be passed to the query. Defaults to ().
            fetchall (bool, optional): Whether to fetch all results. Defaults to True.
            num_rows (int, optional): The number of rows to fetch. Defaults to 0. (Used when fetchall=False)
        Returns:
            dict: The results of the query
        Raises:
            Error: If the query cannot be executed
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        if fetchall:
            result = {}
            for row in cursor.fetchall():
                result[len(result)] = row
            return result
        else:   
            result = {}
            for row in cursor.fetchmany(num_rows):
                result[len(result)] = row
            return result


    def execute_query_as_stored_procedure(self, query, parameters=()):
        """
        Executes a query as a stored procedure

        Args:
            query (str): The query to be executed
            connection (mysql.connector.connection_cext.CMySQLConnection): The connection to the database
            parameters (tuple, optional): The parameters to be passed to the query. Defaults to ().
        Returns:
            dict: The results of the query
        Raises:
            Error: If the query cannot be executed
        """
        cursor = self.connection.cursor()
        cursor.callproc(query, parameters)

    def execute_stored_procedure_with_no_parameters(self, procedure_name, auto_commit=False):
        """
        Executes a stored proedure

        Args:
            procedure_name (str): The filename for the stored procedure 
            connection (mysql.connector.connection_cext.CMySQLConnection): The connection to the database
            auto_commit (bool, optional): Whether to commit the query. Defaults to True.
        Returns:
            cursor: mysql.connector.cursor_cext.CMySQLCursor object        
        Raises:
            Error: If the store procedure cannot be executed
        """
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.callproc(procedure_name)

                # Fetching result set
                result = []
                for result_set in cursor.stored_results():
                    result.extend(result_set.fetchall())

                column_names = list(result[0].keys()) if result else []

                if auto_commit:
                    self.connection.commit()

                return column_names, result
        except Exception as e:
            self.connection.rollback()
            raise e
        
    def execute_stored_procedure(self, procedure_name, parameters=(), auto_commit=False):
        """
        Executes a stored proedure

        Args:
            procedure_name (str): The filename for the stored procedure 
            parameters (tuple, optional): The parameters to be passed to the store procedure. Defaults to ().
            connection (mysql.connector.connection_cext.CMySQLConnection): The connection to the database
            auto_commit (bool, optional): Whether to commit the query. Defaults to True.
        Returns:
            cursor: mysql.connector.cursor_cext.CMySQLCursor object        
        Raises:
            Error: If the store procedure cannot be executed
        print(procedure_name)
        """
        """ with self.connection.cursor() as cursor:
            cursor.callproc(procedure_name, parameters)
            if auto_commit:
                self.connection.commit()
            else:
                return cursor.fetchall()"""
            
        if not isinstance(parameters, tuple):
            raise ValueError("Parameters must be a tuple")

        try:
            with self.connection.cursor(dictionary=True) as cursor:
                #print(parameters)
                cursor.callproc(procedure_name, parameters)

                # Fetching result set
                result = []
                for result_set in cursor.stored_results():
                    result.extend(result_set.fetchall())

                column_names = list(result[0].keys()) if result else []

                if auto_commit:
                    self.connection.commit()

                return column_names, result
        except Exception as e:
            self.connection.rollback()
            raise e
                
