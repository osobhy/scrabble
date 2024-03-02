# scrabble.py
# Omar Sobhy with additional help from Emily Salamanca
# Portions written by David Liben-Nowell for CS 111, Carleton College.
# Modified for Python 3 by Eric Alexander
# Modified in 2023 by Sneha Narayan

import random

def scoreTile(letter):
    '''Given a letter (one of ABCDEFGHIJKLMNOPQRSTUVWXYZ), returns the
       number of points that letter is worth.  Causes an error if it
       is passed a parameter that is not a upper-case letter.'''

    # Check to make sure that letter is really a letter.
    if letter not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        raise ValueError("I can't compute the score of letter " + letter + "!")

    # Each letter is worth some designated number of points.  The list
    # scores records the value of each letter -- the letters in the
    # string scores[i] are each worth exactly i points.
    scores = ['',           # 0 points
              'EAIONRTLSU', # 1 point
              'DG',         # 2 points
              'BCMP',       # 3 points
              'FHVWY',      # 4 points
              'K',          # 5 points 
              '',           # 6 points
              '',           # 7 points
              'JX',         # 8 points
              '',           # 9 points
              'QZ']         # 10 points

    # Look through every string in the scores list until we find letter.
    # If we found letter in scores[i], then the point count for letter is i.
    for i in range(len(scores)):
        if letter in scores[i]:
            value = i
    return value

def scoreWord(word):
    score = 0

    '''Given a word, returns the number of points that word is worth, which
       is the sum of the point counts for each word.  For example:
         scoreWord("ALFAQUI")   --> 19
         scoreWord("DJINN")     --> 13
    
         scoreWord("HEGEMONY")  --> 17'''
    for let in word:
        score = score + scoreTile(let)
    return score

def randomHand(tiles):
    '''Computes a random hand of seven tiles from the original pool.'''
    return random.sample(tiles,7)


def playable(word, hand):
    '''Given a word and a hand, where a word is a string of letters
       and a hand is a list of tiles (which are themselves letters),
       returns True if that word can be played using only the tiles in
       hand and False if not.  For example:
          playable("ADZE", ['Z', 'C', 'E', 'E', 'D', 'T', 'A'])     --> True
          playable("ARIOSE", ['R', 'I', 'S', 'A', 'O', 'I', 'E'])   --> True
          playable("UCALEGON", ['R', 'I', 'S', 'A', 'O', 'I', 'E']) --> False
          playable("AREA", ['A', 'E', 'I', 'O', 'U', 'Y', 'R'])     --> False
       Notice this last example returns False because, although there is an 'A'
       in the hand, the word "AREA" requires *two* 'A's.'''
    hand_copy = []
    hand_copy.extend(hand)

    for char in word:
        if char in hand_copy:
            hand_copy[hand_copy.index(char)] = 0
        elif char not in hand_copy:
            return False
    return True

def loadDictionary():
    ''' Create a list of all words that are legal to play in Scrabble.
        The dictionary file included is the official Scrabble dictionary 
        from a few years ago, so we can accomplish this simply by loading
        each line and adding it to the end of the words list. '''
   
    words = []
    try: 
        dictfile = open("twl98.txt")
    except IOError:
        print("ERROR! twl98.txt doesn't appear in the current directory.")
        print("Please see the assignment instructions.")
        exit(1)
    for line in dictfile:
        word = line.strip() # Removes any whitespace before or after each word in the file.
        words.append(word) # Adds the word to the list "words"
    dictfile.close()
    return words

def allValidPlayable(hand):
    '''Given a hand of tiles and a list of valid words in Scrabble,
       returns the list of words that are playable from that hand, 
       and are also valid words in Scrabble. '''
    words = loadDictionary()
    validWords = []
    for word in words:
        if playable(word, hand):
            validWords.append(word)
    return validWords

def bestPlayable(hand, words):
    '''Given a hand of tiles and a list of valid words in Scrabble,
       returns the highest-scoring valid word that can be played 
       from that hand.'''
    bestScore = -1
    bestWord = ''

    for word in words:
        score = scoreWord(word)
        if playable(word, hand):
            if score > bestScore:
                bestScore = score
                bestWord = word
    return bestWord

def main():
    # The full set of 100 tiles in Scrabble.  (Actually, I'm only giving
    # you 98 of them; two of the real tiles are blanks, which can be used
    # in place of any letter as a wildcard.)
    tiles = 12*['E'] + 9*['A'] + 9*['I'] + 8*['O'] + 6*['N'] + 6*['R'] \
        + 6*['T'] + 4*['L'] + 4*['S'] + 4*['U'] + 4*['D'] + 3*['G'] + 2*['B'] \
        + 2*['C'] + 2*['M'] + 2*['P'] + 2*['F'] + 2*['H'] + 2*['V'] + 2*['W'] \
        + 2*['Y'] + 1*['K'] + 1*['J'] + 1*['X'] + 1*['Q'] + 1*['Z']

    # The list of all legal words in Scrabble
    words = loadDictionary()

    # A random hand drawn from the full set of tiles
    hand = randomHand(tiles)

    print("Here's a random starting hand of Scrabble tiles:", hand)
    print("These are all the valid words you can make from these tiles:", allValidPlayable(hand))
    
    # The best scoring valid word you can play from your hand
    best = bestPlayable(hand, words)
    print("The word from this list with the best Scrabble score is", best, "for", scoreWord(best), "points.")

main()
