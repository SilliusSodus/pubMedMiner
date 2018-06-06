import sys
from flask import Flask, render_template, request
sys.path.insert(0,"/home/owe8_pg4/public_html/Applicatie.1/static/")
from Bio import Entrez
import subprocess
import transform
import re
import ast


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
    
    try:
    	search = request.args.get('search', '')
    
        #cmd = "ls"
        records = getPubmedDocuments("pubmed", search)
    except:
        return "Pubmed has no articles on this subject. Go back and try again with a different search term." 
    
    
    #documents = [i for i in read_input(records)]
    #print (documents)
	
    #markTheCommons(documents)
    mine(['python2.7',"/home/owe8_pg4/public_html/Applicatie.1/tagMining.py"])

    mine(["python3.4","/home/owe8_pg4/public_html/Applicatie.1/mining.py",search])
    
    
    edges = reading('/home/owe8_pg4/public_html/Applicatie.1/currentMining.txt')
    words = reading('/home/owe8_pg4/public_html/Applicatie.1/words.txt')
    
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
                            stdin=subprocess.PIPE)#,shell=True)
    out,err = p.communicate()
    return out, err

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

'''
Haalt de dataset op van pubmed dmv een term
'''
def getPubmedDocuments(db, term):
    Entrez.email = "s.temolder@student.han.nl"
    handle = Entrez.esearch(db=db, term=term, retmax=100000)
    handle2 = Entrez.efetch(db=db, id=Entrez.read(handle)["IdList"], retmode="xml")
    records = Entrez.read(handle2)["PubmedArticle"]
    return records

'''
Haalt de juiste informatie uit de opgehaalde records
'''
def read_input(records):
    for x in records:
        if "Abstract" in x["MedlineCitation"]["Article"].keys() and "ArticleTitle" in x["MedlineCitation"][
            "Article"].keys():
            yield re.findall(r"[\w']+",x["MedlineCitation"]["Article"]["ArticleTitle"] + \
                             x["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0])

