import time
from typing import Coroutine
from rake_nltk import Rake
import operator
import pymongo
import nltk
from bs4 import BeautifulSoup as bs
from nltk import corpus
import os

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
def keyphrase(text):
    r = Rake()
    text = str(text)
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()
    keywithscore = r.get_ranked_phrases_with_scores()
    result = [item[1] for item in keywithscore if item[0] >= 8 ]
    
    return result

def preprocess(text):

    corpus = []
    #lema
    from nltk.stem import WordNetLemmatizer
 
    lem = WordNetLemmatizer()
    text = text.lower()
    text = [lem.lemmatize(word) for word in text]
    text = "".join(text)
    corpus.append(text)

    return corpus

content = []

dir = './patents'
s = os.curdir
print(s)

tic = time.perf_counter()
for filename in os.listdir(dir):

    if filename.endswith(".xml"):
        print(filename)
    
        with open(str(dir) + "/" + str(filename), "r", encoding="utf-8") as file:
            # Read each line in the file, readlines() returns a list of lines
            content = file.readlines()
            # Combine the lines in the list into a string
            content = "".join(content)
            bs_content = bs(content, "lxml")

            result = bs_content.find("p").get_text()
            result = str(result)
            result = result.replace("<br/>","").replace("\n","")
            text = preprocess(result)
            keys = keyphrase(text)

            client = pymongo.MongoClient('mongodb://db:secret@db:27017/?authSource=admin')
            db = client.patent_extractor

            db_obj = { "filename" : filename}

            db_obj["keyphrases"] = keys

            db.patents.insert_one(db_obj)

toc = time.perf_counter()
print(f"Code ended in {toc - tic:0.4f} seconds")




