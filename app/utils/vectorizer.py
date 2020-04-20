from sklearn.feature_extraction.text import TfidfVectorizer
from app.utils import toke
import boto3
import os
import json
import numpy as np
from flask import Flask
app = Flask(__name__)

if os.environ.get("deployment", False):
    app.config.from_pyfile('/etc/cs4300-volume-cfg/cs4300app.cfg')
else:
    app.config.from_pyfile(os.path.join(
        os.path.join(os.getcwd(), "secrets"), "cs4300app.cfg"))

tokenizer = toke.tokenized_already
key = app.config["AWS_ACCESS"]
secret = app.config["AWS_SECRET"]

# P03Data.json
s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret)
s3.download_file('cs4300-data-models', 'P03Data.json', 'P03Data.json')

# S3 JSON Format:
# { "CS4300": {"Piazza": {PostID: content, PostID2: content2}, "Textbook": {DocId: content, DocID2: content2} } }
with open("P03Data.json") as f:
    fromS3 = json.load(f)

docVecDictionary = {}
courseDocDictionary = {}
sourceDictionary = {}
# courseRawDataDictionary = {}
# courseURLDictionary = {}
# courseTypeOfDocDictionary = {}
# courseDocIDNameDictionary = {}

for course in fromS3:
    vec = TfidfVectorizer(tokenizer=tokenizer, lowercase=False)
    documents = []
    src = []
    # rawData = []
    # URL = []
    # typeOfDoc = []
    # docIDName = []
    rawDocs = []
    for source in fromS3[course]:
        for content in fromS3[course][source]:
            # for final in fromS3[course][source][content]:
                #pre is type, first is text, second is tokenized, third is url
            documents.append(fromS3[course][source][content].pop("tokenized"))
            rawDocs.append(fromS3[course][source][content])
            if source == "Piazza":
                src.append(1)
            else:
                src.append(0.1)
                # if final == "type":
                #     typeOfDoc.append(
                #         fromS3[course][source][content][final])
                # elif final == "raw":
                #     rawData.append(fromS3[course][source][content][final])
                # elif final == "tokenized":
                #     documents.append(
                #         fromS3[course][source][content][final])
                # elif final == "url":
                #     URL.append(fromS3[course][source][content][final])
                # elif final == "doc_name":
                #     docIDName.append(
                #         fromS3[course][source][content][final])
    # elif course == "INFO 1998"
    sourceDictionary[course] = np.array(src)
    docVecDictionary[course] = (vec, vec.fit_transform(documents).toarray())
    courseDocDictionary[course] = np.array(rawDocs)
    # [["this", "is", "the", "post"],["Piazza", "this", "is", "the", "post"]]
    # courseDocDictionary[course] = np.array(documents)
    # courseRawDataDictionary[course] = np.array(rawData)
    # courseURLDictionary[course] = np.array(URL)
    # courseTypeOfDocDictionary[course] = np.array(typeOfDoc)
    # courseDocIDNameDictionary[course] = np.array(docIDName)

# print(courseRawDataDictionary["CS 4300"][0])

# docVecDictionary is full dictionary of all documents in all courses. Everything should be a global variable.
