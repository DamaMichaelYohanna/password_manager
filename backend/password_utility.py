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

    def return_generated_password(self):
        """public method to return the generated password"""
        # call the private password generator and return it return value.
        return self.__main_password_generator()

    def password_strength_check(self, password: str):
        lower, upper, char, digit = 0, 0, 0, 0
        capital_alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        small_alphabets = "abcdefghijklmnopqrstuvwxyz"
        special_char = '!"#$%&()*+,-./:;<=>@[]_|'
        digits = "0123456789"
        if not password:
            return 0

        elif len(password) <= 5:
            return 1

        elif len(password) > 5 and password.isdigit() or password.isalpha() or password.islower() or password.isupper():
            print("from here")
            return 2
        elif len(password) > 5 and password.isdigit() or password.isalnum():
            return 3
        if len(password) >= 8:
            for value in password:

                # counting lowercase alphabets
                if value in small_alphabets:
                    lower += 1

                # counting uppercase alphabets
                elif value in capital_alphabets:
                    upper += 1

                # counting digits
                elif value in digits:
                    digit += 1

                # counting the mentioned special characters
                elif value in special_char:
                    char += 1

            if (lower >= 1 and upper >= 1 and
                    char >= 1 and digit >= 1):
                return 10

            if (lower <= 1 and upper <= 1 and
                    char >= 1 and digit >= 1):
                return 9

            if (lower >= 1 and upper >= 1 and
                    char == 1 and digit == 1):
                return 8

            if (lower >= 1 and upper >= 1 and
                    char == 1 and digit == 0):
                return 4.5

            if (lower >= 1 and upper >= 1 and
                    char == 0 and digit == 1):
                return 4.5

            if (lower >= 1 and upper >= 1 and
                    char == 1 or char > 1 and digit == 1):
                return 7



