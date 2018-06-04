import nltk
import re
from app import reading,writeToFile

def bringOutYerDead():
    documents = reading("currentText.txt")
    modelWords = reading("modelWords.txt")

    writeToFile("allWords.txt", dict)

bringOutYerDead()
