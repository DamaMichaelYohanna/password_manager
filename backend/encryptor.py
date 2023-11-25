import string


class Encryptor:
    """A class use for encrypting and decrypting user password,
     using a slightly modified version of cipher wheel
    """

    def __init__(self):
        """ Initial all public variable and make them ready"""

        self.letter_mixed = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E',
                             'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J',
                             'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O',
                             'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T',
                             't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y',
                             'y', 'Z', 'z', ' ']  # make a mixture of letters
        self.letter_mixed.extend(string.punctuation)
        self.letter_mixed.extend(string.digits)

        self.letter_upper_and_lower = list(string.ascii_letters)  # make it an instance var
        self.letter_upper_and_lower.extend(string.digits)
        self.letter_upper_and_lower.extend(string.punctuation)
        self.letter_upper_and_lower.append(' ')

    def __find(self, word, mixed_letters):
        """ This method take a word and find it in letter_mixed then return the
            indexs of each letter in list """
        index = []  # empty list to track index
        for letter in word:  # a for loop
            try:
                a = mixed_letters.index(letter)  # find the index of letter given
                index.append(a)  # append the index to the list index above
            except ValueError:
                # could not find character
                pass
        return index  # return the index lists

    def __swap(self, lists, full_alphabet):
        """ The swap method take a list of index and find the corresponding
                words in self.letter_upper_and_lower after which it return a
                string of all the word it find concatinated together"""

        findings = ''  # Create an empty string
        for numb in lists:  # loop through the index in a for loop
            findings += full_alphabet[numb]  # concatinate the words into findings
        return findings  # return the concatinated words

    def encrypt(self, word):
        """ The encrypt take in word from it caller and in return calls
         self.__swap which also in return calls self.__find. and return
         encrypted word
         """

        encrypted_word = self.__swap(
            self.__find(word, self.letter_mixed),
            self.letter_upper_and_lower)  # call swap method
        return encrypted_word  # return the salted words

    def decrypt(self, word):
        """decrypt the given password"""
        decrypted_word = self.__swap(
            self.__find(word, self.letter_upper_and_lower),
            self.letter_mixed)  # call swap method
        return decrypted_word  # return the salted words

