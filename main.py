# Create a connection class for mysql to store scraped
# items to a mysql database

from __future__ import print_function
from mysql.connector import Error
import mysql.connector
from sqlalchemy import create_engine
import sqlalchemy as sa

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MZMfib112358!#',
    'database': 'scraped',
    'raise_on_warnings': True
}


class MysqlTest:
    table = "scrapy_items"
    host = 'localhost'
    user = 'root'
    port = '3306'
    db = 'scraped'
    password = input("Enter Password: ")
    mysql_connect = f"mysql://{user}:{password}@{host}:{port}/{db}"

    def __init__(self, **kwargs):
        self.engine = create_engine(MysqlTest.mysql_connect, echo=True)
        print("[+] Engine Created...")

    # def _connect_engine(self):
    #     engine = create_engine(self.mysql_connect, echo=True)
    #     print("[+] Engine Created...")
    #     return engine

    # def mysql_connect(self):
    #     try:
    #         return mysql.connector.connect(MysqlTest.config)
    #     except mysql.connector.Error as err:
    #         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #             print("Something is wrong with your username or password...")
    #         elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #             print("Database doesn't exist, could not connect...")
    #         else:
    #             print(err)

    def select_items(self):
        try:
            cursor = self.engine.cursor()
            select_query = "SELECT * FROM " + self.table

            cursor.execute(select_query)
            for row in cursor.fetchall():
                print(row)

            cursor.close()
        except Error as err:
            print(err)

    def insert_items(self, values):
        try:
            cursor = self.engine.cursor()
            insert_query = f"INSERT INTO {self.table} VALUES {values};"

            cursor.execute(insert_query)
            cursor.commit()
            cursor.close()

        except Error as err:
            print(err)


values = """('1', 'The world as we have created it is a process of our thinking.
        It cannot be changed without changing our thinking!', 'Albert Einstein')"""

if __name__ == '__main__':
    mysql = MysqlTest()
    mysql.insert_items(values)
    mysql.select_items()
