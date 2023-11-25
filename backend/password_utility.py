import random
import string


class PasswordManager:
    def __init__(self):
        pass
        # self.db_handle = PasswordDatabase()

    def __main_password_generator(self):
        """ private method to generate the password"""
        password = ''  # create an empty string to store password
        # create a big string containing all the strings in upper and lower case
        # as well as the punctuation marks.
        big_string = '!"#$%&()*+,-./:;<=>@[]_|' + string.ascii_letters + string.digits
        for i in range(16):  # create a for loop 16 times
            # randomly get a letter or number or punctuation from the big string
            # and add it to the password string
            password += big_string[random.randint(0, len(big_string) - 1)]
        return password  # return the password
    #
    # def __main_password_saver(self, site_name, username, password, encrypted, owner):
    #     """private method to call the database handle and save new password"""
    #     self.db_handle.save_record(site_name, username, password, encrypted, owner)
    #
    # def __main_single_password_retriever(self, site_name, user_id):
    #     """
    #     private method to call the db handle
    #     and get one record from database.
    #     Requires a site name to perform query
    #      """
    #     return self.db_handle.get_single_record(site_name, user_id=user_id)
    #
    # def __main_all_password_retriever(self, user_id):
    #     """private method to call db handle and retrieve all the db entries"""
    #     return self.db_handle.retrieve_all_records(user_id=user_id)

    def return_generated_password(self):
        """public method to return the generated password"""
        # call the private password generator and return it return value.
        return self.__main_password_generator()
    #
    # def save_new_password(self, site_name, username, password, owner, encrypt=True, ):
    #     """call the private save password
    #     method and passing the received inputs
    #     """
    #     if encrypt:
    #         # call the encryptor call and encrypt the password
    #         password = Encryptor().encrypt(password)
    #         encrypted = 'true'  # set encrypt flag to string true
    #     else:
    #         encrypted = 'false'  # set encrypt flat to string false if not encrypted
    #     self.__main_password_saver(site_name, username, password, encrypted, owner)
    #     return None
    #
    # def retrieve_single_password(self, site_name, user_id):
    #     result = self.__main_single_password_retriever(site_name=site_name,
    #                                                    user_id=user_id)
    #     result = list(result)
    #     if result[4] == 'true':
    #         # call the decryptor  and decrypt the password
    #         result[3] = Encryptor().decrypt(result[3])
    #     else:
    #         pass  # pass if password was not encrypted
    #     return result
    #
    # def retrieve_all_password(self, user_id):
    #     """public method to call the private method for retrieving all password"""
    #     # get all records and convert it to list, then decrypt the encrypted
    #     # passwords before sending to the front end.
    #     results = self.__main_all_password_retriever(user_id=user_id)
    #     arrange_list = []
    #     for result in results:  # use for loop to transverse the password
    #         # convert to list because tuple don't allow assignment
    #         result = list(result)
    #         if result[4] == 'true':
    #             # call the decryptor  and decrypt the password
    #             result[3] = Encryptor().decrypt(result[3])
    #             arrange_list.append(result)
    #         # if not encrypted before, just pass
    #     return arrange_list
    #
    # def delete_single_record(self, pk):
    #     """call the db class delete function passing it the records pk"""
    #     return self.db_handle.delete_single_record(pk)
    #
    # def delete_all_records(self):
    #     """call the db class drop table function to clear records"""
    #     return self.db_handle.drop_table()
    #
    # def update_password(self, pk, site_name, username, password, encrypt, owner):
    #     if encrypt:  # if the user ticks the encrypt check button
    #         # call the encryptor class and encrypt the password
    #         password = Encryptor().encrypt(password)
    #         encrypted: str = 'true'  # set encrypted flag to string true
    #     else:
    #         encrypted = 'false'  # set encrypted flat to string false if not encrypted
    #     self.db_handle.update_record(pk, site_name, username, password, encrypted, owner)
