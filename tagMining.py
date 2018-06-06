import sys
sys.path.insert(0,"/home/owe8_pg4/public_html/Applicatie.1/")
sys.path.insert(0,"/home/owe8_pg4/public_html/Applicatie.1/static")
sys.path.insert(0,"/home/owe8_pg4")
sys.path.insert(0, '/usr/local/lib/python3.4/site-packages')
#from nltk import FreqDist,word_tokenize,pos_tag,download
import nltk
nltk.data.path.append("/home/owe8_pg4/nltk_data")
nltk.download('punkt',download_dir="/home/owe8_pg4/nltk_data")
nltk.download('maxent_treebank_pos_tagger',download_dir="/home/owe8_pg4/nltk_data")
nltk.download('averaged_perceptron_tagger',download_dir="/home/owe8_pg4/nltk_data")
sys.path.insert(0,"/home/owe8_pg4/nltk_data")
import ast

#import nltk
import re


#from app import reading,writeToFile

'''
Haalt de onnodige woorden uit het huidige model. Alleen de nouns, adjectives, woorden die minder dan 50 keer voorkomen en 3 woorden of korter zijn of 9 woorden of langer
'''
def markTheCommons():
    documents = reading('/home/owe8_pg4/public_html/Applicatie.1/records.txt')
    text = " ".join([" ".join(i) for i in documents])
    freqDist = nltk.FreqDist(re.findall(r"[\w']+", text))
    writeToFile("/home/owe8_pg4/public_html/Applicatie.1/freqDist.txt",str(dict(freqDist)))
    print("here1")
    # open('test.txt', "w+").write(str(freqDist.keys()))
    #download('maxent_treebank_pos_tagger')
    NNJJ = []
    #download('maxent_treebank_pos_tagger',download_dir="/home/owe8_pg4/public_html/Applicatie.1")
    print("here2")
    start = nltk.word_tokenize(text)
    print("here2.5")
    tokens = nltk.pos_tag(start)
    print("here3")
    for x in tokens:
        if "NN".__eq__(x[1]) or "JJ".__eq__(x[1]):
            NNJJ.append(x[0])
    #print(str(NNJJ))
    print("here4")
    writeToFile("/home/owe8_pg4/public_html/Applicatie.1/NNJJ.txt",str(NNJJ))

'''
Schrijft stuffToWrite naar een file
'''
def writeToFile(fileName, stuffToWrite):
    file = open(fileName, "w+")
    file.write(str(stuffToWrite))
    file.close()


'''
Leest een bestand in en zet het in een standaard python object.
'''
def reading(name):
    with open(name, 'r') as f:
        s=f.read()
        pythonObject = ast.literal_eval(s)
    return pythonObject

markTheCommons()
