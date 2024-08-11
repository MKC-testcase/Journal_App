import unittest
import os
import datetime

print(os.getcwd())
from model.access_database import *


class DatabaseAccessTestcase(unittest.TestCase):
    def test_insert(self):
        db = DB(server_name='Marcus_Comp', database="Alexandria", user_name="Marcus", password="1234")
        sql_statement = f"INSERT INTO [Alexandria].[dbo].Journal ([date], [entry]) VALUES('{datetime.datetime.now().strftime('%Y-%m-%d')}',  'This is a test')"
        db.set_connection()
        db.create_cursor()
        response = db.send_data(sql_statement)
        self.assertEqual(response, True)
        db.end_connection()

    def test_delete(self):
        db = DB(server_name='Marcus_Comp', database="Alexandria", user_name="Marcus", password="1234")
        sql_statement = f"DELETE FROM Alexandria.dbo.Journal WHERE date = '{datetime.datetime.now().strftime('%Y-%m-%d')}';"
        db.set_connection()
        db.create_cursor()
        response = db.send_data(sql_statement)
        self.assertEqual(response, True)
        db.end_connection()


if __name__ == "__main__":
    unittest.main()

    # print(response)
