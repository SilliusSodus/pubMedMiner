#import nltk
#from app import writeToFile,reading
import sys
import gensim
#from gensim.models.word2vec import *
from Bio import Entrez
import re
from itertools import chain
import ast


'''
Textminet pubmed op compounds en zet de resultaten in 2 files
'''
def mining():

    search = sys.argv[1]
    #print(search)
    #preprocessing

    records = getPubmedDocuments("pubmed",search)
    documents = [i for i in read_input(records)]
    #Textmining
    model = gensim.models.Word2Vec(documents,size=150,window=10,min_count=20,workers=10)
    model.train(documents, total_examples=len(documents), epochs=20)
    #open('test2.txt','w+').write("textmining done")

    NNJJ = reading('/home/owe8_pg4/public_html/Applicatie.1/NNJJ.txt')
    freqDist = reading('/home/owe8_pg4/public_html/Applicatie.1/freqDist.txt')

    #processing
    words = bringOutYerDead(model,freqDist,NNJJ)
    #print("Text mining done")

    #Writing to files
    sims = getSims(model, words)
    dict = getPubLinks(sims, records)
    writeToFile("/home/owe8_pg4/public_html/Applicatie.1/currentMining.txt", dict)


    uniqueWords = set(list(chain.from_iterable([i.split(" ") for i in sims.keys()])))
    #open("test3.txt", "w+").write(str(uniqueWords))
    wordsDict = {}
    for word in uniqueWords:
        wordsDict[word] = 1
    writeToFile("/home/owe8_pg4/public_html/Applicatie.1/words.txt",wordsDict)
    print("done")

'''
Haalt de juiste informatie uit de opgehaalde records
'''
def read_input(records):
    for x in records:
        if "Abstract" in x["MedlineCitation"]["Article"].keys() and "ArticleTitle" in x["MedlineCitation"][
            "Article"].keys():
            yield gensim.utils.simple_preprocess(x["MedlineCitation"]["Article"]["ArticleTitle"] + \
                             x["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0])


def bringOutYerDead(model,freqDist,NNJJ):
    dict = {}
    for x in freqDist:
        if freqDist[x] < 50 and x in model.wv.index2word and x in NNJJ and (len(x) < 4 or len(x) > 8):
            dict[x] = freqDist[x]
    return dict

'''
Voegt de waarden van gelijkheid toe aan de edges
'''
def getSims(model, words):
    dict = {}
    done = []
    #file = open('test2.txt', "w+")
    for x in words:
        for y in words:
            if y not in done:
                if x is not y:
                    sim = model.wv.similarity(x, y)*10
                    if sim > 6:
                        dict["" + x + " " + y] = [sim]

        done.append(x)
    return dict


'''
Voegt de links naar pubmed toe aan de edges
'''
def getPubLinks(dictWords, records):
    for words in dictWords.keys():
        if dictWords[words][0] > 0:
            for record in records:
                if "Abstract" in record["MedlineCitation"]["Article"].keys() and "ArticleTitle" in \
                        record["MedlineCitation"]["Article"].keys():
                    text = record["MedlineCitation"]["Article"]["ArticleTitle"] + \
                           record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]
                    if words.split(" ")[0] in text and words.split(" ")[1] in text:
                        dictWords[words].append(int(record["MedlineCitation"]["PMID"]))
                if len(dictWords[words]) > 5:
                    continue

        if len(dictWords[words]) < 2:
            dictWords[words].append(1)
    #print("All be good")
    return dictWords

	
'''
Haalt de dataset op van pubmed dmv een term
'''	
def getPubmedDocuments(db,term):
    Entrez.email = "s.temolder@student.han.nl"
    handle = Entrez.esearch(db=db, term = term, retmax=100000)
    handle2 = Entrez.efetch(db=db, id = Entrez.read(handle)["IdList"], retmode="xml")
    return Entrez.read(handle2)["PubmedArticle"]	
	
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


mining()
