import os
import sys
from flask import Flask, render_template, request
from Bio import Entrez
import subprocess
import transform
#import DataBaseSanne
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("casa.html")

@app.route('/Submit', methods=["GET"])
def Submit():
    print("Started")
    search = request.args.get('search', '')
    #cmd = "ls"
    mine(["python3.4","mining.py",search])
    
    
    edges = reading('currentMining.txt')
    words = reading('words.txt')
    
    transform.writetograph(words,edges) #str(dict)
    time.sleep(5)
    return render_template("visualisatie.html")

def mine(cmd):

    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out, err

import ast

def reading(name):
    with open(name, 'r') as f:
        s=f.read()
        pythonObject = ast.literal_eval(s)
    return pythonObject

def writeToFile(fileName, stuffToWrite):
    file = open(fileName, "w+")
    file.write(str(stuffToWrite))
    file.close()


if __name__ == '__main__':
    app.run()
