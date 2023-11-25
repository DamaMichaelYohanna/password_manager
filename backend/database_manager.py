import sqlite3



class PasswordDatabase:
    """class for database transactions and queries"""

    def __init__(self):
        """ class initializer method. create db table as well."""
        # create table statement.
        sql_statement = """CREATE TABLE passwordTable 
        (pk INTEGER PRIMARY KEY,'sitename', 'username', 'password', 'encrypted', owner INTEGER)"""
        try:  # try creating the table
            self.cursor(sql_statement)
        # if error error occurred due to table already existing, just pass
        except sqlite3.OperationalError:
            pass

    def cursor(self, sql):
        """
        open the database connection using context manager
        and grab the cursor as well for execution of queries.
        requires one positional parameter: which should be a string
        of valid sql query .
        """
        with sqlite3.connect('db.sqlite3') as conn:  # open connection
            cursor = conn.cursor()  # grab the cursor
            result = cursor.execute(sql)  # execute the given query.
            conn.commit()  # commit the executed transaction
            return result  # return result.

    def save_record(self, sitename, username, password, encrypted, owner):
        """save record to db"""
        sql_statement = f""" INSERT INTO passwordTable ('sitename', 'username', 'password', 'encrypted', 'owner') 
        VALUES ('{sitename}', '{username}', '{password}', '{encrypted}', {owner})
        """  # prepare sql statement
        self.cursor(sql_statement)  # call cursor to execute query.

    def retrieve_all_records(self, user_id):
        """Grab all data from database for the lock in user"""
        # prepared sql query
        sql_statement = f'SELECT * FROM passwordTable WHERE owner = {user_id}'
        result = self.cursor(sql_statement)  # call cursor to execute query
        return result.fetchall()

    def get_single_record(self, sitename, user_id):
        """get all single record from the database. requires a valid site name"""
        sql_statement = f"""SELECT * FROM passwordTable WHERE sitename='{sitename}' AND owner = {user_id}"""
        result = self.cursor(sql_statement)  # call cursor to execute query
        return result.fetchone()  # return result

    def drop_table(self):
        """delete all records in the db"""
        sql_statement = 'DROP TABLE passwordTable'
        self.cursor(sql_statement)
        return None

    def delete_single_record(self, pk):
        """delete a single entry from the db. requires a site name"""
        sql_statement = f"""DELETE FROM passwordTable WHERE pk='{pk}'"""
        self.cursor(sql_statement)
        return None

    def update_record(self, pk, sitename, username, password, encrypted, owner):
        """method to update records in the database given the pk"""
        sql_statement = f"""
                UPDATE passwordTable SET ('sitename', 'username', 'password', 'encrypted', 'owner') 
                =('{sitename}', '{username}', '{password}', '{encrypted}',  '{owner}') WHERE pk={pk}
                """  # prepare sql statement
        self.cursor(sql_statement)  # call cursor to execute query.
        return None


class UserDatabase:
    """class to manage users records for authentication"""

    def __init__(self):
        """ class initializer method. create db table as well."""
        # create table statement.
        sql_statement = """CREATE TABLE userTable 
        (pk INTEGER PRIMARY KEY, username VARCHAR UNIQUE, 'password')"""
        # sql_statement2 = 'DROP TABLE userTable'
        # self.cursor(sql_statement2)
        try:  # try creating the table
            self.cursor(sql_statement)
        # if error error occurred due to table already existing, just pass
        except sqlite3.OperationalError as e:
            pass

    def cursor(self, sql):
        """
        open the database connection using context manager
        and grab the cursor as well for execution of queries.
        requires one positional parameter: which should be a string
        of valid sql query .
        """
        with sqlite3.connect('db.sqlite3') as conn:  # open connection
            cursor = conn.cursor()  # grab the cursor
            result = cursor.execute(sql)  # execute the given query.
            conn.commit()  # commit the executed transaction
            return result  # return result.

    def save_login_details(self, username, password):
        """save record to db"""
        sql_statement = f"""
        INSERT INTO userTable ('username', 'password') VALUES ('{username}', '{password}')
        """  # prepare sql statement
        try:
            self.cursor(sql_statement)  # call cursor to execute query.
            error = False
        except sqlite3.IntegrityError:
            error = True
        finally:
            return error

    def all_user(self):
        sql_statement = """SELECT * FROM userTable"""
        result = self.cursor(sql_statement)

    def login(self, username, password):
        sql_statement = f"""SELECT pk, username, password FROM userTable WHERE username='{username}'"""
        result = self.cursor(sql_statement)  # perform query
        result = result.fetchone()  # grab a single entry from the return values
        if not result:  # username not found
            return 0  # return zero for failed
        else:  # if username exist, check if pasword matches
            if password == result[2]:  # compare the given and saved password
                return result[0]  # return passed if they are the same
            else:
                return 0  # return zero if not the same
