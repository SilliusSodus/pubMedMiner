#import os
#import sys
from flask import Flask, render_template, request
#from Bio import Entrez
import subprocess
import transform
#import DataBaseSanne
#import time

app = Flask(__name__)

'''
Begint de applicatie
'''
@app.route('/')
def index():
    return render_template("Home.html")


'''
runt al de textmining, voor meer info zie mining.py
'''
@app.route('/Submit', methods=["GET"])
def Submit():
    print("Started")
    search = request.args.get('search', '')
    #cmd = "ls"
    mine(["python3.4","mining.py",search])
    
    
    edges = reading('currentMining.txt')
    words = reading('words.txt')
    
    transform.writetograph(words,edges) #str(dict)
    #time.sleep(1000)
    #print(str(open("static/js/graph.js").read()))
    return render_template("visualisatie.html")

'''
Roept een andere .py file aan dmv een terminal command zodat er andere python interpreters gebruikt kunnen worden
'''
def mine(cmd):

    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out, err

import ast


'''
Leest een bestand in en zet het in een standaard python object.
'''
def reading(name):
    with open(name, 'r') as f:
        s=f.read()
        pythonObject = ast.literal_eval(s)
    return pythonObject

'''
Schrijft stuffToWrite naar een file
'''
def writeToFile(fileName, stuffToWrite):
    file = open(fileName, "w+")
    file.write(str(stuffToWrite))
    file.close()


if __name__ == '__main__':
    app.run()
