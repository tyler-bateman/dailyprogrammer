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


# Populates matchesList with the list of possible words for the given encoded message
def smorse(encodedString):
    smorseRecursive(encodedString, '')

# Populates matchesList with the list of words that are possible given the
# solved portion of the word and the encoded fragment remaining.
# If encodedFragment is 0, the solved portion is tested against the word list
# and perhaps added to the list. Otherwise, it calls itself recursively
def smorseRecursive(encodedFragment, solvedPortion):
    if len(encodedFragment) is 0:
        if solvedPortion + '\n' in wordlist:

            matchesList.append(solvedPortion)
            #print(solvedPortion)
        ## TODO: Validate solutions in the master list
    else:
        for i in range(1, min(len(encodedFragment) + 1, 5)):
            curLetter = encodedFragment[:i]
            if curLetter in codeDictionary:
                smorseRecursive(encodedFragment[i:], solvedPortion + codeDictionary[curLetter])


f = open("wordlist.txt", "r")
wordlist = f.readlines()

masterCodeString = '.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --.. '
codeDictionary = parseCodes(masterCodeString)
matchesList = list()
smorse(sys.argv[1])
for item in matchesList:
    print item

# for pair in codeDictionary:
#     print(pair + ': ' + codeDictionary[pair] )
