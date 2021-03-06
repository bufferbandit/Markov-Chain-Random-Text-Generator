import sys,docx
import os.path
from random import choice

END_PUNCTATION = ["!","?","."]

DEBUG = False #True

def generateDict(text):
    words = text.split()
    if len(words) > 2:
        dictionary = {}
        for i,w in enumerate(words):
            firstWord = words[i];
            try:    #try to get the other words, maybe i am at the end of the list
                secondWord = words[i+1];
                thirdWord = words[i+2];
            except: #we don't care if we don't have words following the current one and then we exit the loop
                break

            key = (firstWord,secondWord)

            if key not in dictionary:   #this pair of words is new to the dictionary, and so doesn't have a list of following words
                dictionary[key]  = []

            dictionary[key].append(thirdWord)

        return dictionary
    else:
        return None

def getStartingKey(dictionary):
    #only upper cased first-in-tuple words are valid for a startingKey 
    possibleStartingKeys = [key for key in list(dictionary.keys()) if key[0][0].isupper()] 
    startingKey = choice(possibleStartingKeys)
    return startingKey

def generateText(dictionary):

    startingKey = getStartingKey(dictionary)

    sentence = []
    sentence.append(startingKey[0])
    sentence.append(startingKey[1])

    sentences = 0
    key = startingKey
    while True:
        try:
            possibleWords = dictionary[key]
            chosenWord = choice(possibleWords)

            key = (key[1],chosenWord)
            #print(chosenWord, end=" ")

            if DEBUG and len(possibleWords)>1:   #with DEBUG enabled you will see a colored word when the word was chosen from a more-than-1 choice list, aka the sentence could have gone 2 or more ways.
                sentence.append("\033[94m" + chosenWord + "\033[0m")
                print("\'" + chosenWord + "\' from " + str(possibleWords))
            else:
                sentence.append(chosenWord)

            if chosenWord[-1] in END_PUNCTATION:    #if the last char of the word is a end sentence thing
                sentence.append("\n")
                sentences = sentences + 1
                if sentences > int(sys.argv[2]):
                    break 

        except KeyError:    #the path is closed, better start another sentence!
            key = getStartingKey(dictionary)
            sentence.append("\n")
            sentence.append(key[0])
            sentence.append(key[1])
       
       #print(sentence[-1], end=" ")
       # print(key)

    return " ".join(sentence)


#main
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ./markov.py <input> <sentences> <output>")
    else:
        fileName = sys.argv[1]
        doc = docx.Document() 
        doc_para = doc.add_paragraph('')
        if os.path.isfile(fileName):
            with open(fileName, 'r') as inputFile:
                text = inputFile.read()
                dictionary = generateDict(text)
                if dictionary:
                    text = generateText(dictionary)
                    #print("\n\n--Result--\n\n" + text)
                    with open(sys.argv[3]+".txt","a" ) as f:
                       f.write(text) 
                       doc_para.add_run(text)
                       doc.save(sys.argv[3]+".doc")
                    #doc.save('path_to_document') 
                else:
                    print("Can't generate dictionary from the input text.\nERROR in generateDict.")
        else:
            print(fileName + " not found. Please check if file exists.")   
