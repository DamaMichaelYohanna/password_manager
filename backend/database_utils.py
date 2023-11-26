from backend import database, encryptor


class DatabaseUtility:
    def __init__(self):
        self.database_handle = database.DatabaseOps()
        self.encrypt_handle = encryptor.Encryptor()

    def insert_user_login(self, username, password, question, answer):
        statement = """INSERT INTO User ('username', 'password', 'question', 'answer') VALUES (?, ?,?,?)"""
        values = (username, password, question, answer)
        return self.database_handle.insert_record(statement, values)

    def login(self, username, password):
        sql_statement = f"""SELECT pk, username, password FROM User WHERE username='{username}'"""
        user = self.database_handle.fetch_record(sql_statement).fetchone()
        if not user:
            return 0  # return zero if user not found
        else:  # if user exist, check if password matches
            if password == user[2]:  # compare the given and saved password
                return [user[0], user[1]]  # return username and id
            else:
                return 0  # return zero if not the same

    def insert_password(self, sitename, username, password, owner):
        password = self.encrypt_handle.encrypt(password)
        sql_statement = f"""
                INSERT INTO Login ('sitename', 'username', 'password', 'owner') 
                VALUES (?, ?, ?, ?)
                """
        parameter = (sitename, username, password, owner)
        print(parameter)
        self.database_handle.insert_record(sql_statement, parameter)

    def insert_note(self, title, content, owner):
        """function to prepare the sql statement and call the needed function"""
        content = self.encrypt_handle.encrypt(content)
        sql_statement = """
                INSERT INTO Notes ('title', 'content', 'owner') 
                VALUES (?, ?, ?)
                """
        parameter = (title, content, owner)
        self.database_handle.insert_record(sql_statement, parameter)

    def insert_payment(self, bank_name, pin, account, owner):
        sql_statement = f"""
                INSERT INTO Payments ('bank', 'pin', 'number', 'owner') 
                VALUES (?, ?, ?, ?)
                """
        parameter = (bank_name, pin, account, owner)
        self.database_handle.insert_record(sql_statement, parameter)

    # --------------------------------------------------------------------------------------
    # fetch section of our database utilities

    def fetch_data(self, table, owner, pk: int | None = None):
        if not pk:
            statement = f"""SELECT * FROM {table} WHERE owner={owner}"""
        else:
            statement = f"""SELECT * FROM {table} WHERE owner={owner} AND pk={pk}"""
        return_values = self.database_handle.fetch_record(statement)
        return return_values

    # ---------------------------------------------------------------------------------------
    # delete section for our database utilities
    def delete_record(self, table, pk, owner):
        """delete a single entry from the db. requires a site name"""
        sql_statement: str = f"""DELETE FROM {table} WHERE pk= ? AND owner= ? """
        parameter: tuple = (pk, owner)  # create parameter tuple
        self.database_handle.delete_record(sql_statement, parameter)
        return None

    # --------------------------------------------------------------------------------------------
    # update section for different data
    def update_note(self, title, content, pk, owner):
        content = self.encrypt_handle.encrypt(content)
        sql_statement = f"""
                        UPDATE Notes SET ('title', 'content') 
                        =(?, ?) WHERE pk={pk} AND owner={owner}
                        """  # prepare sql statement
        parameter = (title, content)
        self.database_handle.update_record(sql_statement, parameter)

    def update_payment(self, bank_name, bank_pin, account_number, pk, owner):
        bank_name = self.encrypt_handle.encrypt(bank_name)
        bank_pin = self.encrypt_handle.encrypt(bank_pin)
        sql_statement = f"""
                        UPDATE Payments SET ('bank', 'pin', 'number') 
                        =(?, ?, ?) WHERE pk=? AND owner=?
                        """  # prepare sql statement
        parameter = (bank_name, bank_pin, account_number, pk, owner)
        self.database_handle.update_record(sql_statement, parameter)

    def update_password(self, sitename, password, owner,
                        username: str | None = None,
                        pk: str | None = None):

        """function to update stored login password. Not current user password"""
        password = self.encrypt_handle.encrypt(password)
        if username and pk:
            sql_statement = f"""
                        UPDATE Login SET ('sitename', 'password', 'password') 
                        = (?, ?, ?) WHERE owner=? AND pk=?
                        """
            parameter = (sitename, username, password, owner, pk)

        else:
            sql_statement = f"""
                        UPDATE Login SET ('password') = (?) WHERE sitename= ? AND owner= ?
                        """
            parameter = (sitename, password, owner)
        self.database_handle.update_record(sql_statement, parameter)
