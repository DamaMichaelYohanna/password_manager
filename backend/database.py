import os.path
import sqlite3
from pathlib import Path

from backend import encryptor


class DatabaseOps:
    def __init__(self):
        file_path = Path(__file__).resolve().parent
        self.conn = sqlite3.connect(os.path.join(file_path, "23storage.sqlite3"))
        self.cursor = self.conn.cursor()
        self.encrypt_handle = encryptor.Encryptor()
        self.set_up()

    def set_up(self):
        sql_list = [

            "CREATE TABLE IF NOT EXISTS User (pk INTEGER PRIMARY KEY, username VARCHAR UNIQUE, 'password')",
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

    def save_login_details(self, username, password):
        """save record to db"""
        sql_statement = f""" INSERT INTO User ('username', 'password') VALUES ('{username}', '{password}')
        """  # prepare sql statement
        try:
            self.cursor.execute(sql_statement)  # call cursor to execute query.
            self.conn.commit()
            error = False
        except sqlite3.IntegrityError:
            error = True
        finally:
            return error

    def login(self, username, password):
        sql_statement = f"""SELECT pk, username, password FROM User WHERE username='{username}'"""
        result = self.cursor.execute(sql_statement)  # perform query
        result = result.fetchone()  # grab a single entry from the return values
        if not result:  # username not found
            return 0  # return zero for failed
        else:  # if username exist, check if password matches
            if password == result[2]:  # compare the given and saved password
                return [result[0], result[1]]  # return passed if they are the same
            else:
                return 0  # return zero if not the same












    def save_password(self, sitename, username, password, encrypted, owner):
        """save record to db"""
        password = self.encrypt_handle.encrypt(password)
        sql_statement = f"""
        INSERT INTO Login ('sitename', 'username', 'password', 'encrypted', 'owner') 
        VALUES ('{sitename}', '{username}', '{password}', '{encrypted}', {owner})
        """  # prepare sql statement
        self.cursor.execute(sql_statement)  # call cursor to execute query.
        self.conn.commit()  # commit changes to database

    def retrieve_all_records(self, user_id):
        """Grab all data from database for the logged-in user"""
        # prepared sql query
        sql_statement = f'SELECT * FROM Login WHERE owner = {user_id}'
        result = self.cursor.execute(sql_statement)  # call cursor to execute query
        return result.fetchall()

    def get_single_record(self, sitename, user_id):
        """get all single record from the database. requires a valid site name"""
        sql_statement = f"""SELECT * FROM Login WHERE sitename='{sitename}' AND owner = {user_id}"""
        result = self.cursor.execute(sql_statement)  # call cursor to execute query
        return result.fetchone()  # return result

    def delete_single_record(self, pk, owner):
        """delete a single entry from the db. requires a site name"""
        sql_statement = f"""DELETE FROM Login WHERE pk='{pk}' AND owner='{owner}'"""
        self.cursor.execute(sql_statement)
        return None

    # def update_record(self, pk, sitename, username, password, encrypted, owner):
    #     """method to update records in the database given the pk"""
    #     password = self.encrypt_handle.encrypt(password)
    #     sql_statement = f"""
    #             UPDATE Login SET ('sitename', 'username', 'password', 'encrypted', 'owner')
    #             =('{sitename}', '{username}', '{password}', '{encrypted}',  '{owner}') WHERE pk={pk}
    #             """  # prepare sql statement
    #     self.cursor.execute(sql_statement)  # call cursor to execute query.
    #     self.conn.commit()
    #     return None

    def update_password(self, sitename, password, owner):
        """method to update password in the database given the sitename"""
        password = self.encrypt_handle.encrypt(password)
        sql_statement = f"""
                UPDATE Login SET password='{password}' WHERE sitename='{sitename}' AND owner='{owner}'
                """
        self.cursor.execute(sql_statement)  # call cursor to execute query.
        self.conn.commit()
        return None



obj = DatabaseOps()
# "INSERT INTO Term (name) VALUES ('Second')",
# "INSERT INTO Term (name) VALUES ('Third')"
# obj.save_login_details('Dama', '123456')
# obj.insert_record("INSERT INTO Subject (name, class) VALUES ('Mathematics', 'JSS 1');")
# obj.insert_record("INSERT INTO Subject (name, class) VALUES ('Basic Science', 'JSS 1');")
# obj.conn.commit()
# obj.insert_record("INSERT INTO Class (name) VALUES ('JSS 2');")
# obj.insert_record("INSERT INTO Class (name) VALUES ('JSS 3');")
# obj.insert_record("INSERT INTO Class (name) VALUES ('SSS 1');")
# obj.insert_record("INSERT INTO Class (name) VALUES ('SSS 2');")
# obj.insert_record("INSERT INTO Class (name) VALUES ('SSS 1');")
# obj.insert_record("INSERT INTO Subject (name, grade, division) VALUES ('Civil Education', 'senior', 'all');")
# obj.insert_record("INSERT INTO Subject (name, grade, division) VALUES ('Mathematics', 'senior', 'all');")
# obj.insert_record("INSERT INTO Subject (name, grade, division) VALUES ('Chemistry', 'senior', 'science');")
# obj.insert_record("INSERT INTO Score (student, subject, assignment, test1, test2, exam, total) VALUES ('Gabriel', 'Chemistry', 10, 10, 10, 70, 100);")
# obj.insert_record("INSERT INTO Score (student, subject, assignment, test1, test2, exam, total) VALUES ('Gabriel', 'Physics', 10, 10, 10, 70, 100);")
# obj.insert_record("INSERT INTO Score (student, subject, assignment, test1, test2, exam, total) VALUES ('Gabriel', 'Mathematics', 10, 10, 10, 70, 100);")
# obj.insert_record("""INSERT INTO Student (name, age, sex, state)
#             VALUES ('name', 'age', 'male', 'state');""")
