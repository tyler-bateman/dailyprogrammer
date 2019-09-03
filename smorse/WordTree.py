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




def buildWordTree():
    for word in wordlist:
        #print word
        masterWordTree.insertWord(word[:len(word) - 1])
    #print 'build word tree'


#Create the word tree based on the word list
f = open("wordlist.txt", "r")
wordlist = f.readlines() # A list containing every word in wordlist.txt
masterWordTree = wordTree('', False)
buildWordTree()
masterWordTree.printTree(0)
#Pickle the complete tree
import pickle
wordTreeFile = open('Word_Tree_Object.obj', 'w')
pickle.dump(masterWordTree, wordTreeFile)


# masterWordTree.insertWord('hello')
# masterWordTree.insertWord('goodbye')
# masterWordTree.insertWord('good')
# masterWordTree.insertWord('hi')
# masterWordTree.insertWord('goodboy')
# masterWordTree.insertWord('hellos')
# masterWordTree.printTree(0)
