import nltk
import sys
from gensim.models.word2vec import *
from Bio import Entrez

def mining():
    search = sys.argv[1]
    print(search)
    
    record = getPubmedDocuments("pubmed", search)
    # print(record[1]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0])
    sentences = []
    for x in record:
        if "Abstract" in x["MedlineCitation"]["Article"].keys() and "ArticleTitle" in x["MedlineCitation"][
            "Article"].keys():
            sentences.append((x["MedlineCitation"]["Article"]["ArticleTitle"] +
                              x["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]).split())
    model = Word2Vec(sentences, size=10, window=20, min_count=20, workers=10)
    words = disposeOfTheCommons(model, sentences)
    print("Text mining done")
    wordDict = {}
    for word in words:
        wordDict[word] = 1
    dict = getPubLinks(getSims(model, words), record)
    
    file = open("/home/owe8_pg4/public_html/Applicatie.1/currentMining.txt", "w+")
    file.write(str(dict))
    #file.write(""+str(wordDict))
    file.close()
    
    file1 = open("/home/owe8_pg4/public_html/Applicatie.1/words.txt", "w+")
    file1.write(str(wordDict))
    file1.close()

def disposeOfTheCommons(model, sentences):
    dict = {}
    for x in model.wv.index2word:
        dict[x] = 0
    length = 0
    for x in sentences:
        length += len(x)
        for y in x:
            if y in model.wv.index2word:
                dict[y] += 1
    words = []

    for x in dict.keys():

        if float(dict[x] / length) < float(30 / length):
            words.append(x)

        if len(words) > 20:
            return words
        # return words
    return words

def getSims(model, words):
    dict = {}
    for x in words:
        for y in words:
            if x is not y:
                dict["" + x + " " + y] = [model.wv.similarity(x, y)]
    return dict

def getPubLinks(dictWords, records):
    for words in dictWords.keys():
        for record in records:
            if "Abstract" in record["MedlineCitation"]["Article"].keys() and "ArticleTitle" in \
                    record["MedlineCitation"]["Article"].keys():
                text = record["MedlineCitation"]["Article"]["ArticleTitle"] + \
                       record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]
                for word in words.split(" "):
                    if word in text:
                        dictWords[words].append(int(record["MedlineCitation"]["PMID"]))

        if len(dictWords[words]) < 2:
            dictWords[words].append(1)
    print("All be good")
    return dictWords

def getPubmedDocuments(db, term):
    Entrez.email = "s.temolder@student.han.nl"
    handle = Entrez.esearch(db=db, term=term, retmax=100000)
    handle2 = Entrez.efetch(db=db, id=Entrez.read(handle)["IdList"], retmode="xml")
    return Entrez.read(handle2)["PubmedArticle"]

mining()
