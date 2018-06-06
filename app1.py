import os
import sys
from flask import Flask, render_template, request
from Bio import Entrez
import subprocess
import transform
import DataBase

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("Home.html")

@app.route('/Submit', methods=["GET"])
def Submit():
    print("Started")
    search = request.args.get('search', '')
    #cmd = "ls"
    mine(search)


    edges = reading('currentMining.txt')
    words = reading('words.txt')

    transform.writetograph(words,edges) #str(dict)
    return render_template("visualisatie.html")

def mine(searchWord):
    cmd = ["python3.4", "/home/owe8_pg4/public_html/Applicatie.1/mining.py" ,str(searchWord)]
    #cmd = ["python3.4", "mining.py", str(searchWord)]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return err

import ast

def reading(name):
    with open("/home/owe8_pg4/public_html/Applicatie.1/" + name, 'r') as f:
    #with open(name, 'r') as f:
        s=f.read()
        pythonObject = ast.literal_eval(s)
    return pythonObject

'''
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

        if float(dict[x]/length) < float(30/length):
            words.append(x)

        if len(words) >20:
            return words
        #return words
    return words


def getSims(model,words):
    dict = {}
    for x in words:
        for y in words:
            if x is not y:
                dict[""+ x + " " + y] = [model.wv.similarity(x,y)]
    return dict

def getPubLinks(dictWords,records):
    for words in dictWords.keys():
        for record in records:
            if "Abstract" in record["MedlineCitation"]["Article"].keys() and "ArticleTitle" in record["MedlineCitation"]["Article"].keys():
                text = record["MedlineCitation"]["Article"]["ArticleTitle"] + record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]
                for word in words.split(" "):
                    if word in text:
                        dictWords[words].append(int(record["MedlineCitation"]["PMID"]))

        if len(dictWords[words]) < 2:
            dictWords[words].append(1)
    print("All be good")
    return dictWords




def getPubmedDocuments(db,term):
    Entrez.email = "s.temolder@student.han.nl"
    handle = Entrez.esearch(db=db, term = term, retmax=100000)
    handle2 = Entrez.efetch(db=db, id = Entrez.read(handle)["IdList"], retmode="xml")
    return Entrez.read(handle2)["PubmedArticle"]

'''

@app.route('/database')
def database():
    DataBase.loadFromDatabase(reading('currentMining.txt'),reading('words.txt'))
    return str("Hello something is working")

if __name__ == '__main__':
    app.run()

