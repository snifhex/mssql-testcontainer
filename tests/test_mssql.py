import unittest

from mssql_testcontainer import SQLServerContainer

class TestSQLServerContainer(unittest.TestCase):
    image = "mcr.microsoft.com/mssql/server:2019-latest"
    port = 1433
    sa_password = "YourPass@1"
    database = "tempdb"
    username = "SA"

    @classmethod
    def setUpClass(cls):
        cls.mssql = SQLServerContainer(image = cls.image, port = cls.port,
                                        sa_password = cls.sa_password,
                                        database = cls.database,
                                        username = cls.username)
        cls.mssql.__enter__()
        
    @classmethod
    def tearDownClass(cls):
        cls.mssql.__exit__(None, None, None)

    def test_get_connection_string(self):
        expected_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server=localhost,{self.port};Database={self.database};UID={self.username};PWD={self.sa_password}"
        string = self.mssql._generate_connection_string()
        self.assertEqual(string, expected_string)

    def test_get_connection_url(self):
        expected_url = f"mssql+pyodbc:///?odbc_connect=Driver={{ODBC Driver 17 for SQL Server}};Server=localhost,{self.port};Database={self.database};UID={self.username};PWD={self.sa_password}"
        url = self.mssql.get_connection_url()
        self.assertEqual(url, expected_url)


if __name__ == '__main__':
    unittest.main()
