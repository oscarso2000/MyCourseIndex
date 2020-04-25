import json
import pickle

import boto3
import nltk
from tqdm import tqdm
import html2text

from app.utils.simstring_doc import (
    CharNgramFeatureExtractor,
    RamDatabase,
    CosineSimilarity,
    Searcher
)
from app.utils.toke import sp


s3 = boto3.client('s3')
s3.download_file('cs4300-data-models', 'P03Data_mod.json', 'P03Data.json')

with open("P03Data.json") as fp:
    P03Data = json.load(fp)

db = RamDatabase(CharNgramFeatureExtractor(3))

h = html2text.HTML2Text()
h.ignore_links = True

# map them with triplet keys (course, Piazza/Resource, Key)
# This is encoded as COURSE|RESOURCE|KEY
bigram_2_str = lambda w: w[0] + " " + w[1]
trigram_2_str = lambda w: w[0] + " " + w[1] + " " + w[2]

# Parse Textbook data first
for key, item in tqdm(P03Data["CS 4300"]["Resource"].items(), desc="Resource", leave=True):
    raw = item["raw"]
    tokenized = sp(raw.lower())
    tokenized = [w.text for w in tokenized if not w.is_punct]
    bigrams = nltk.bigrams(tokenized)
    trigrams = nltk.trigrams(tokenized)
    location = "CS 4300|Resource|" + key
    for w in tqdm(tokenized, leave=False, desc="Single words"):
        db.add(w, location)
    for w in tqdm(bigrams, leave=False, desc="Bigrams"):
        db.add(bigram_2_str(w), location)
    for w in tqdm(trigrams, leave=False, desc="Trigrams"):
        db.add(trigram_2_str(w), location)

for post_id, post in tqdm(P03Data["CS 4300"]["Piazza"].items(), leave=True, desc="Piazza"):
    post = post["raw"]
    all_text = ""
    subject = h.handle(post['history'][0]['subject']).replace("\n", " ")
    question = h.handle(post['history'][0]['content']).replace("\n", " ")
    other_text = ""
    for answer in post['children']:
        if answer['type'] == "i_answer":
            other_text += " " + h.handle(answer['history'][0]['content']).replace("\n", " ")
        elif answer['type'] == "s_answer":
            other_text += " " + h.handle(answer['history'][0]['content']).replace("\n", " ")
        elif answer['type'] == "followup": 
            other_text += " " + h.handle(answer['subject']).replace("\n", " ")
            for fb in answer['children']:
                other_text += " " + h.handle(fb['subject']).replace("\n", " ")
    
    all_text = subject + " " + question + " " + other_text
    tokenized = sp(all_text.lower())
    tokenized = [w.text for w in tokenized if not w.is_punct]
    bigrams = nltk.bigrams(tokenized)
    trigrams = nltk.trigrams(tokenized)
    location = ("CS 4300", "Piazza", post_id)
    for w in tqdm(tokenized, leave=False, desc="Single words"):
        db.add(w, location)
    for w in tqdm(bigrams, leave=False, desc="Bigrams"):
        db.add(bigram_2_str(w), location)
    for w in tqdm(trigrams, leave=False, desc="Trigrams"):
        db.add(trigram_2_str(w), location)

indexer = Searcher(db, CosineSimilarity())

with open("ramDB.pkl", "wb") as fp:
    pickle.dump(db, fp)
