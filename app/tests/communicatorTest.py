import unittest
from unittest.mock import patch, Mock
import mysql.connector
from dbCommunicator import load_db_config, create_connection, execute_query

class TestCommunicator(unittest.TestCase):

    @patch('dbCommunicator.mysql.connector.connect')
    def test_create_connection(self, mock_connect):
        """
        Test that create_connection returns a connection object
        """
        mock_connect.return_value = Mock()
        connection = create_connection()
        self.assertIsNotNone(connection)
        mock_connect.assert_called_once()
    
