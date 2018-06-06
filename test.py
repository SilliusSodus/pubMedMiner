import nltk
import os
from flask import Flask, render_template, request
import sys
import subprocess


app = Flask(__name__)

@app.route('/')
def index():
    #log = os.popen("python3.4 mining.py 'bitter gourd'").read()
    #subprocess.call([data["log"], ">", diz['d']+"/points.xml"])
    #cmd = ["python3.4", "/home/owe8_pg4/public_html/Applicatie.1/mining.py" ,'bitter gourd']
    #cmd = "pwd"
    #p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    #out,err = p.communicate()
    return "Yay"

if __name__ == '__main__':
    app.run()
