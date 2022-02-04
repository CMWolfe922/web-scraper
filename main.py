# Create a connection class for mysql to store scraped
# items to a mysql database

from __future__ import print_function
from mysql.connector import errorcode
import mysql.connector
from sqlalchemy import create_engine

class MysqlTest:
    table = "scrapy_items"
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'MZMfib112358!#',
        'database': 'scraped',
        'raise_on_warnings': True
    }

    def __init__(self, **kwargs):
        self.cnx = self.mysql_connect()

    def mysql_connect(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your username or password...")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist, could not connect...")
            else:
                print(err)

    def select_items(self):
        cursor = self.cnx.cursor()
        select_query = "SELECT * FROM " + self.table

        cursor.execute(select_query)
        for row in cursor.fetchall():
            print(row)

        cursor.close()
        self.cnx.close()

def main():
    mysql = MysqlItems()
    mysql.select_items()

if __name__ == '__main__': main()