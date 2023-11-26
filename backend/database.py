import os.path
import sqlite3
from pathlib import Path

from backend import encryptor


class DatabaseOps:
    def __init__(self):
        file_path = Path(__file__).resolve().parent
        self.conn = sqlite3.connect(os.path.join(file_path, "23storage.sqlite3"))
        self.cursor = self.conn.cursor()
        self.set_up()

    def set_up(self):
        sql_list = [

            "CREATE TABLE IF NOT EXISTS User (pk INTEGER PRIMARY KEY, username VARCHAR UNIQUE, password VARCHAR, question VARCHAR, answer VARCHAR)",
            "CREATE TABLE IF NOT EXISTS Login (pk INTEGER PRIMARY KEY, sitename CHAR, username CHAR, password CHAR, owner INTEGER)",
            "CREATE TABLE IF NOT EXISTS Payments  (pk INTEGER PRIMARY KEY, bank CHAR, pin CHAR, number CHAR, owner INTEGER)",
            'CREATE TABLE IF NOT EXISTS Notes  (pk INTEGER PRIMARY KEY, title CHAR, content CHAR, owner INTEGER)',

        ]
        for sql in sql_list:
            self.cursor.execute(sql)
            self.conn.commit()

    def insert_record(self, sql_statement, parameter):
        try:
            self.cursor.execute(sql_statement, parameter)  # call cursor to execute query.
            self.conn.commit()
            return False
        except sqlite3.IntegrityError:
            return True

    def fetch_record(self, sql_statement):
        """function to execute the fetch record command"""
        result = self.cursor.execute(sql_statement)  # call cursor to execute query.
        return result

    def delete_record(self, sql_statement, parameter):
        """function to execute the fetch record command"""
        self.cursor.execute(sql_statement, parameter)  # call cursor to execute query.
        self.conn.commit()
        return None

    def update_record(self, sql_statement, parameter):
        try:
            self.cursor.execute(sql_statement, parameter)  # call cursor to execute query.
            self.conn.commit()
            return False
        except sqlite3.IntegrityError:
            return True

