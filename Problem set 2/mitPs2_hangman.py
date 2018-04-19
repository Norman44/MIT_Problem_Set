# Problem Set 2, hangman.py
# Edited with Visual Studio Code
# Name: Andrew
# Collaborators: 
# Time spent: 

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    count = 0
    for i, c in enumerate(secret_word):
      if c in letters_guessed:
        count += 1
    if count == i+1:
      return True
    else:
      return False
    
def outof_guesses(guesses, secret_word):
    if guesses <= 0:
      print("-----------------")
      print("Sadly you lost, the word was:", secret_word)
      return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    out_list = []
    for i, c in enumerate(secret_word):
      if c in letters_guessed:
        #count += 1
        out_list.insert(i, c)
      else:
        out_list.insert(i, '_ ')
    
    str1 = ''.join(out_list)
    return str1




def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet_list = list(string.ascii_lowercase)
    alphabet_list_copy = alphabet_list[:]
    for i in alphabet_list_copy:
      if i in letters_guessed:
        alphabet_list.remove(i)
    
    str1 = ''.join(alphabet_list)
    return str1



def in_secretword(secret_word, lett):
    for i in range(0, len(secret_word)):
      if secret_word[i]==lett:
        return True




def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    vowels = ['a','e','i','o','u']
    guesses = 20
    warnings = 3
    #secret_word = "else"
    # available_Letters = string.ascii_lowercase
    # play = True
    letters_guessed = []
    i = 0
    #secret_word = choose_word(wordlist)
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("You have", warnings, "warnings.")
    

    while is_word_guessed(secret_word, letters_guessed) == False:
      #secret_word_list = list(secret_word)

      print("------------------------")
      print("You have", guesses, "guesses left")
      #print("You have", warnings, "warnings left")
      print("Available letters:", get_available_letters(letters_guessed))
      lett = input("Please guess a letter: ")

      if str.isalpha(lett):
        str.lower(lett) 
        if lett not in get_available_letters(letters_guessed):
          if warnings == 0:
            guesses -= 1
            print("Oops! You guessed the letter", lett, "already. You have no warnings left") 
            print("so you loose one guess:",get_guessed_word(secret_word, letters_guessed))
          else:
            warnings -= 1
            print("Oops! You guessed the letter", lett, "already. You now have",warnings,
            "warnings left.")
            print(get_guessed_word(secret_word, letters_guessed))
          
        else:
          letters_guessed.insert(i, lett)
          if in_secretword(secret_word, lett):
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
            if is_word_guessed(secret_word, letters_guessed):
              print("------------------------")
              print("Congratulations, you won!")
              print("Total score for this game is:", guesses * len(''.join(set(secret_word))))
          else:
            if lett in vowels:
              guesses -= 2
              print("Oops! The letter", lett, 
              "is not in the secret word and it's a vowel. Therefore you loose 2 guesses.", 
              get_guessed_word(secret_word, letters_guessed))
              if outof_guesses(guesses, secret_word):
                break
            else: 
              guesses -= 1
              print("Oops! The letter", lett, "is not in my word.", get_guessed_word(secret_word, letters_guessed))
              
              if outof_guesses(guesses, secret_word):
                break

      else:
        if warnings == 0:
          guesses -= 1
          print("Oops! The sign", lett, "is not a valid letter. You have", guesses, 
          "guesses left.", get_guessed_word(secret_word, letters_guessed))
          if outof_guesses(guesses, secret_word):
            break
        else:
          warnings -= 1
          print("Oops! The sign", lett, "is not a valid letter. You have", warnings, 
          "warnings left.", get_guessed_word(secret_word, letters_guessed))
          
        i += 1




# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_copy = my_word.replace(" ", "")
    letters_used = [c for c in my_word_copy if c.isalpha()]

    if len(my_word_copy) != len(other_word):
        return False
        
    for i, c in enumerate(my_word_copy):
        if my_word_copy[i] == '_':
            if other_word[i] in letters_used:
                return False
            else:
                continue
        elif my_word_copy[i] == other_word[i]:
            continue
        
        return False

    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = ""
    
    for word in wordlist:
      if match_with_gaps(my_word, word):
        matches += word + " "
    if len(matches) == 0:
      print("No possible matches found.")
    else:
      print(matches) 




def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    vowels = ['a','e','i','o','u']
    guesses = 20
    warnings = 3
    letters_guessed = []
    i = 0

    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("You have", warnings, "warnings.")
    

    while is_word_guessed(secret_word, letters_guessed) == False:

      print("------------------------")
      print("You have", guesses, "guesses left")
      print("For a hints press \"*\" ")
      print("Available letters:", get_available_letters(letters_guessed))
      lett = input("Please guess a letter: ")

      if str.isalpha(lett):
        str.lower(lett) 
        if lett not in get_available_letters(letters_guessed):
          if warnings == 0:
            guesses -= 1
            print("Oops! You guessed the letter", lett, "already. You have no warnings left") 
            print("so you loose one guess:",get_guessed_word(secret_word, letters_guessed))
          else:
            warnings -= 1
            print("Oops! You guessed the letter", lett, "already. You now have",warnings,
            "warnings left.")
            print(get_guessed_word(secret_word, letters_guessed))
        else:
          letters_guessed.insert(i, lett)
          if in_secretword(secret_word, lett):
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
            if is_word_guessed(secret_word, letters_guessed):
              print("------------------------")
              print("Congratulations, you won!")
              print("Total score for this game is:", guesses * len(''.join(set(secret_word))))
          else:
            if lett in vowels:
              guesses -= 2
              print("Oops! The letter", lett, 
              "is not in the secret word and it's a vowel. Therefore you loose 2 guesses.", 
              get_guessed_word(secret_word, letters_guessed))
              if outof_guesses(guesses, secret_word):
                break
            else: 
              guesses -= 1
              print("Oops! The letter", lett, "is not in my word.", get_guessed_word(secret_word, letters_guessed))
              if outof_guesses(guesses, secret_word):
                break

      elif lett == "*":
        print("Possible word matches are: ")
        show_possible_matches(secret_word)

      else:
        if warnings == 0:
          guesses -= 1
          print("Oops! The sign", lett, "is not a valid letter. You have", guesses, 
          "guesses left.", get_guessed_word(secret_word, letters_guessed))
          if outof_guesses(guesses, secret_word):
            break
        else:
          warnings -= 1
          print("Oops! The sign", lett, "is not a valid letter. You have", warnings, 
          "warnings left.", get_guessed_word(secret_word, letters_guessed))
          
        i += 1



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
     #pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
