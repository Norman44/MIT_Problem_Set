# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        #valid_words_copy = self.valid_words 
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        lower_case = string.ascii_lowercase
        upper_case = string.ascii_uppercase
        
        if shift < 0:
            shift = abs(shift)
        shift = shift % 26

        normal_letters = upper_case + lower_case
        shift_letters = upper_case[shift:] + upper_case[:shift] + lower_case[shift:] + lower_case[:shift]
        return dict(zip(normal_letters, shift_letters))

        
        # # Second version:

        # shift_dict = {
        #     **{k: upper_case[(i + shift) % 26] for i, k in enumerate(upper_case)},
        #     **{k: lower_case[(i + shift) % 26] for i, k in enumerate(lower_case)}
        #     # '**' means "treat the key-value pairs in the dictionary as additional named arguments to this function call."
        # }
        # return shift_dict



    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        message_list = list(self.message_text)
        shifted_dictionary = self.build_shift_dict(shift)
        unchange = [' '] + list(string.punctuation)
        for i, c in enumerate(message_list):
            if c not in unchange and c in shifted_dictionary:
                message_list[i] = shifted_dictionary[c]
        return ''.join(message_list)

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        #self.encryption_dict = copy_encryption_dict
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted  

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text) 
        #self.valid_words = load_words(WORDLIST_FILENAME) 

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        """
        #Uncompleted solution
        #w_list = []
        d = {}
        for s in range(0, 27):
            real_words_lst = []
            count = 0
            w_list = self.apply_shift(s).split()
            for i in w_list:
                if is_word(self.get_valid_words(), i):
                    real_words_lst.append(i) 
                    #print(real_words_lst)
                    #count += 1
                    d[s] = real_words_lst
                    #print(d)
                    #print(s, w_list)
                    #d[s] = w_list
            #     else:
            #         real_words_lst.append(i)

            # if count > 0:
            #     real_words_lst.append(count)
            #     d[s] = real_words_lst    

        mx = max(d.values(), key = len)
        #print(mx)
        for key, value in d.items():
            if value == mx:
                if key == 0:
                    return key, ' '.join(value)
                return key, ' '.join(value)
        """
        mess = self.message_text         
        shift = 0
        words = '' 
        words_correct = 0 
            
        for s in range(26):
            count = 0                               
            words = self.apply_shift(s).split()            
                            
            for c in words:
                if is_word(self.valid_words, c):
                   count += 1
                         
            if count >= words_correct:
               words_correct = count
               shift = s
            self.message_text = mess  
                        
        words = self.apply_shift(shift)   
        
        return (shift, words) 


def decrypt_story():
    txt = CiphertextMessage(get_story_string())
    txt1 = txt.decrypt_message()

    return txt1

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())

    #Example test case (CiphertextMessage)
    # ciphertext = CiphertextMessage('jgnnq')
    # print('Expected Output:', (24, 'hello'))
    # print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE
    txt = PlaintextMessage('Olesia is gay!', 5)
    print(txt.get_message_text_encrypted())
    txt1 = CiphertextMessage(txt.get_message_text_encrypted())
    print(txt1.decrypt_message())


    #TODO: best shift value and unencrypted story 

    #print(decrypt_story())
  
