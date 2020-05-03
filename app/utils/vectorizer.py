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


def create_reverse_index(lst):
    d = {}
    for i, w in enumerate(lst):
        d[w] = i
    return d


tokenizer = toke.tokenized_already
key = app.config["AWS_ACCESS"]
secret = app.config["AWS_SECRET"]

# P03Data.json
s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret)
s3.download_file('cs4300-data-models', 'P03Data_mod.json', 'P03Data.json')

# S3 JSON Format:
# { "CS4300": {"Piazza": {PostID: content, PostID2: content2}, "Textbook": {DocId: content, DocID2: content2} } }
with open("P03Data.json") as f:
    fromS3 = json.load(f)

docVecDictionary = {}
courseDocDictionary = {}
sourceDictionary = {}
courseRevsereIndexDictionary = {}
tokenized_dict = {}
foldersDictionary = {}
svdDictionary = {}

for course in fromS3:
    vec = TfidfVectorizer(tokenizer=tokenizer, lowercase=False)
    documents = []
    src = []
    # rawData = []
    # URL = []
    # typeOfDoc = []
    # docIDName = []
    rawDocs = []
    folders = []
    for source in fromS3[course]:
        for content in fromS3[course][source]:
            documents.append(fromS3[course][source][content].pop("tokenized"))
            rawDocs.append(fromS3[course][source][content])
            if source == "Piazza":
                src.append(1)
                folders.extend(fromS3[course][source][content].get("raw").get("folders"))
            else:
                folders.append("Resource")
                src.append(0.2) # Warning, magic number

    foldersDictionary[course] = list(set(folders))
    vecArr = vec.fit_transform(documents).toarray()
    tokenized_dict[course] = documents
    sourceDictionary[course] = np.array(src)
    docVecDictionary[course] = (vec, vecArr)
    courseDocDictionary[course] = np.array(rawDocs)
    courseRevsereIndexDictionary[course] = create_reverse_index(vec.get_feature_names())
    svdDictionary[course] = np.linalg.svd(vecArr.T) #svd on tfidf documents
