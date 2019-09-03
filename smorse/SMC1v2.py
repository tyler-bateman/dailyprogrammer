# The following code is a solution to the problem posed by the reddit thread
# found at the url in URL.txt

# Author: Tyler Bateman
# Start date: 8/16/19
# End date: TBD


import math
import sys

# Generates a dictionary containing each letter and its corresponding morse code
# param codeString: a string containing morse code letters separated by spaces
def parseCodes(codeString):
    curCode = ''
    curLetter = 97 #ASCII code for 'a'
    dictionary = dict()
    for c in codeString:
        if c is ' ':
            dictionary[curCode] = chr(curLetter)
            curCode = ''
            curLetter += 1
        else:
            curCode = curCode +  c
    return dictionary

def reverseDictionary(dictionary):
    newDict = dict()
    for item in dictionary:
        newDict[dictionary[item]] = item
    return newDict


# Populates matchesList with the list of possible words for the given encoded message
def smorse(encodedString):
    matchesList = list()
    smorseRecursive(encodedString, '')

# Populates matchesList with the list of words that are possible given the
# solved portion of the word and the encoded fragment remaining.
# If encodedFragment is 0, the solved portion is tested against the word list
# and perhaps added to the list. Otherwise, it calls itself recursively
def smorseRecursive(encodedFragment, solvedPortion):
    if len(encodedFragment) is 0:
        if masterWordTree.contains(solvedPortion):
            matchesList.append(solvedPortion)
            #print(solvedPortion)

    else:
        for i in range(1, min(len(encodedFragment) + 1, 5)):
            curLetter = encodedFragment[:i]
            if curLetter in codeDictionary:
                smorseRecursive(encodedFragment[i:], solvedPortion + codeDictionary[curLetter])

def encode(word):
    code = ''
    for letter in word:
        code += letterDictionary[letter]
    return code

def buildSectionedWordList(): #Obsolete
    curWord = 0
    sectList = list()

    for i in range(0, 26):

        letterWordList = list()
        while wordlist[curWord][:1] is chr(i + 97):
            letterWordList.append(wordlist[curWord])
            curWord += 1
        sectList.append(letterWordList)

    return sectList



# Defines the data structure in which the list of words will be stored.
# Words are stored in a tree where the words in each level have one more letter
#   than the one before. The tree stores all sequences of letters leading up to
#   a word, so nodes store whether they are a valid word with an isWord field.
#
# Provided I implemented it correctly, the Big O runtime for searching should be
# based on the length of the word being searched rather than the number of words
# in the list. This is a drastic improvement. However, there is a large overhead
# involved in actually building the structure. Since the structure will be the
# same every time it is run, I will try to find a way to store it externally
# rather than rebuild it on every run.
class wordTree:
    def __init__(self, wordBase, isWord):
        self.wordBase = wordBase # The sequence of letters that make up the base of this tree. All children will start with this sequence.
        self.isWord = isWord # Boolean that denotes whether the wordBase is itself a word.
        self.children = list() # A list of wordTrees (The children of this node)


    def insertWord(self, word):
        #print self.wordBase
        # Store the length of the word to be inserted and the length of the word base of this node
        wordLength = len(word)
        wordBaseLength = len(self.wordBase)
        if word[:wordBaseLength] == self.wordBase: # It is invalid to insert a word that does not start with the word base of this node.
            if word == self.wordBase:
                # If the word to be inserted is identical to this word base, simply set isWord to true
                self.isWord = True
            else:
                # If the node has an existing child in which to insert the word, do so.
                # Otherwise, create a new node and insert it there.
                hasCorrectChild = False
                for child in self.children:
                    if word[:len(child.wordBase)] == child.wordBase:
                        child.insertWord(word)
                        hasCorrectChild = True
                        break
                if not hasCorrectChild:
                    newChild = wordTree(word[:wordBaseLength + 1], False)
                    newChild.insertWord(word)
                    self.children.append(newChild)

    # Returns whether the tree contains the given word.
    # O(len(word)) runtime
    def contains(self, word):
        if self.wordBase == word:
            return self.isWord
        else:
            for child in self.children:
                if child.wordBase == word[:len(child.wordBase)]:
                    return child.contains(word)
            return False

    def printTree(self, depth):
        pWord = self.wordBase
        if self.isWord:
            pWord = pWord + '*'
        for i in range(0, depth):
            pWord = '  ' + pWord
        print pWord

        for child in self.children:
            child.printTree(depth + 1)

def filterListByLength(wList, length):
    newList = list()
    for word in wList:
        if len(word) is length:
            newList.append(word)

def buildWordTree():
    for word in wordlist:
        print word
        masterWordTree.insertWord(word[:len(word) - 1])
    print 'built word tree'

def printMatches():
    for match in matchesList:
        print match

#################################################################################
#The remaining functions solve the bonus challenges on the original reddit post.#
#################################################################################

# Bonus challenge 1: Find the only sequence that's the code for 13 different words

def bonusChallenge1():
    print 'Solving bonus challnge 1...'
    occ = dict()
    for word in wordlist:
        print word
        matchesList = list()
        encoding = encode(word.strip())
        if(encoding in occ):
            occ[encoding] += 1
            if occ[encoding] is 13:
                print 'solution found!'
                print encoding
                smorse(encoding)
                printMatches()
                return encoding
        else:
            occ[encoding] = 1

# Bonus challenge 2: Find the only word that has 15 dashes in a row
def bonusChallenge2():
    for word in wordlist:
        word = word.strip()
        morse = encode(word)
        numDashes = 0
        for symbol in morse:
            if symbol is '-':
                numDashes += 1
                if numDashes is 15:
                    print word
                    return word
            else:
                numDashes = 0
    print 'no solution found'

# Bonus challenge 3: Find the two 21 letter words that are perfectly balanced
def bonusChallenge3():
    solutionList = list()
    for word in wordlist:
        word = word.strip()
        if len(word) is 21:
            encoding = encode(word)
            numDot = 0;
            numDash = 0;
            for symbol in encoding:
                if symbol is '.':
                    numDot += 1
                else:
                    numDash += 1
            if numDot is numDash:
                solutionList.append(word)
    return solutionList

# Bonus challenge 4: Find the only 13 letter word that encodes to a palindrome
def bonusChallenge4():
    for word in wordlist:
        word = word.strip()
        if len(word) is 13 and isPalindrome(encode(word)):
            return word

def isPalindrome(word):
    for i in range(0, (len(word) + 1) / 2):
        if word[i] != word[len(word) - 1 - i]:
            return False
    return True

# Bonus challenge 5: Find the five 13-character sequences that do not appear in the encoding of any word
#def bonusChallenge5:
def bonusChallenge5():
    sequenceList = list()
    length = 13
    for i in range(0, int(math.pow(2, length))):
        sequence = str(bin(i))[2:].replace('0', '.').replace('1', '-')
        while len(sequence) < length:
            sequence = '.' + sequence
        sequenceList.append(sequence)

    for word in wordlist:
        if len(word) < 13 and len(word) > 3:
            seq = encode(word.strip())
            if seq in sequenceList:
                sequenceList.remove(seq)

    return sequenceList



import math
def generateAllSequence(length):


    return sequenceList




##########################
print 'reading wordlist.txt...'
f = open("wordlist.txt", "r")
wordlist = f.readlines()
print 'done'
##########################

##########################
print 'loading word tree...'
import pickle
file_word_tree = open('Word_Tree_Object.obj', 'r')
masterWordTree = pickle.load(file_word_tree)
#masterWordTree.printTree(0)
print 'done'
#####################

#######################
print'loading morse code dictionary...'
masterCodeString = '.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --.. '
codeDictionary = parseCodes(masterCodeString)
letterDictionary = reverseDictionary(codeDictionary)
print 'done'
########################
matchesList = list()

arg = sys.argv[1]

if arg is '1':
    bonusChallenge1()
elif arg is '2':
    bonusChallenge2()

elif arg is '3':
    solution = bonusChallenge3()
    for word in solution:
        print word
elif arg is '4':
    solution = bonusChallenge4()
    print solution
elif arg is '5':
    results = bonusChallenge5()
    for s in results:
        print s
else:
    print 'finding matches...'

    smorse(sys.argv[1])
    printMatches()
