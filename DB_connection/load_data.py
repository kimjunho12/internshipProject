#  load_data.py
import pandas as pd
import pymysql

from DB_connection import dbconfig


class LoadData:
    def __init__(self):
        self.db = dbconfig.MysqlController(
            host='192.168.1.241', id='intoai', pw='intoai66!', db_name='208')
        self.cursor = self.db.cursor

    def show_db_version(self):
        # execute SQL query using execute() method.
        self.cursor.execute("SELECT VERSION()")
        # Fetch a single row using fetchone() method.
        data = self.cursor.fetchone()
        print("Database version : %s " % data)

    def select_data(self, sql):
        query = sql
        df = pd.read_sql(query, self.db.conn)
        return df

    def close(self):
        self.db.close()
