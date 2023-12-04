from dbCommunicator import DBConnector
import json
import os

# get scope of ../data/ to import linparser.py
path = '../data/'
os.chdir(path)


class Utils:
    """
    This class contains utility functions.
    """

    @staticmethod
    def toJSON(result):
        """
        This function converts a result to a JSON object.

        Args:
            result (dict): The result to convert

        Returns:
            JSON: The converted result
        """
        return json.dumps(result, default=str)

        

def shell():
    """
    This function is used to run the shell.
    """
    db = DBConnector()
    while True:
        print("Enter a query or 'q' to exit the shell:")
        query = input()
        if query == "q":
            break
        result = db.execute_query(query)
        print(result)
