import mysql.connector
from mysql.connector import Error
import json

def load_db_config(filename):
    """
    Load database configuration from a JSON file

    Args:
        filename (str): The name of the JSON file containing the configuration

    Returns:
        dict: database configuration    
    """
    with open(filename, 'r') as file:
        return json.load(file)

db_config = load_db_config('../db_config.json')

def create_connection():
    """
    creates DB connection

    Returns:
        connection: mysql.connector.connection_cext.CMySQLConnection object
    Raises:
        Error: If the connection cannot be established 
    """
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Error: '{e}'")
    return connection

def execute_query(query, connection, parameters=(), auto_commit=True):
    """
    Executes DB query

    Args:
        query (str): The query to be executed
        parameters (tuple, optional): The parameters to be passed to the query. Defaults to ().
        connection (mysql.connector.connection_cext.CMySQLConnection): The connection to the database
        auto_commit (bool, optional): Whether to commit the query. Defaults to True.
    Returns:
        cursor: mysql.connector.cursor_cext.CMySQLCursor object        
    Raises:
        Error: If the query cannot be executed

    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, parameters)
        if auto_commit:
            connection.commit()
            print("Query executed successfully")
        else:
            return cursor
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_stored_procedure(procedure_name, connection, parameters=(), auto_commit=True):
    """
    Executes a stored proedure

    Args:
        procedure_name (str): The filename for the stored procedure 
        parameters (tuple, optional): The parameters to be passed to the store procedure. Defaults to ().
        connection (mysql.connector.connection_cext.CMySQLConnection): The connection to the database
    Returns:
        cursor: mysql.connector.cursor_cext.CMySQLCursor object        
    Raises:
        Error: If the store procedure cannot be executed
    """
    cursor = connection.cursor()
    try:
        cursor.callproc(procedure_name, parameters)
        if auto_commit:
            connection.commit()
            print("Store procedure executed successfully")
        else:
            return cursor
    except Error as e:
        print(f"The error '{e}' occurred")


# BEGIN TEST SCRIPT
connection = create_connection()
# print connection info
print(connection)

