from sklearn.feature_extraction.text import TfidfVectorizer
from app.utils import toke
import boto3
import os
import json
import numpy as np
from tqdm import tqdm
import io
from flask import Flask
import logging
app = Flask(__name__)

if os.environ.get("deployment", False):
    app.config.from_pyfile('/etc/cs4300-volume-cfg/cs4300app.cfg')
else:
    app.config.from_pyfile(os.path.join(
        os.path.join(os.getcwd(), "secrets"), "cs4300app.cfg"))

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


class TqdmToLogger(io.StringIO):
    """
        Output stream for TQDM which will output to logger module instead of
        the StdOut.
    """
    logger = None
    level = None
    buf = ''
    def __init__(self,logger,level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO
    def write(self,buf):
        self.buf = buf.strip('\r\n\t ')
    def flush(self):
        self.logger.log(self.level, self.buf)


app.logger.debug("Begin Vectorizer")
tqdm_out = TqdmToLogger(app.logger,level=logging.INFO)

def create_reverse_index(lst):
    d = {}
    for i, w in enumerate(lst):
        d[w] = i
    return d


tokenizer = toke.tokenized_already
key = app.config["AWS_ACCESS"]
secret = app.config["AWS_SECRET"]

# P03Data.json
app.logger.debug("Things initialized")
s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret)
s3.download_file('cs4300-data-models', 'P03Data_mod_concepts.json', 'P03Data.json')
app.logger.debug("Data downloaded")

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

app.logger.debug("Pre For loop")

for course in tqdm(fromS3, file=tqdm_out, mininterval=30,desc="Course"):
    vec = TfidfVectorizer(tokenizer=tokenizer, lowercase=False)
    documents = []
    src = []
    # rawData = []
    # URL = []
    # typeOfDoc = []
    # docIDName = []
    rawDocs = []
    folders = []

    for source in tqdm(fromS3[course], file=tqdm_out, mininterval=30,desc="Source"):
        for content in tqdm(fromS3[course][source], file=tqdm_out, mininterval=30,desc="Content"):
            documents.append(fromS3[course][source][content].pop("tokenized"))
            rawDocs.append(fromS3[course][source][content])
            if source == "Piazza":
                src.append(1)
                folders.extend(fromS3[course][source][content].get("raw").get("folders"))
            else:
                # folders.append("Resource")
                src.append(0.2) # Warning, magic number

    foldersDictionary[course] = sorted(list(set(folders)))
    vecArr = vec.fit_transform(documents).toarray()
    tokenized_dict[course] = documents
    sourceDictionary[course] = np.array(src)
    docVecDictionary[course] = (vec, vecArr)
    courseDocDictionary[course] = np.array(rawDocs)
    courseRevsereIndexDictionary[course] = create_reverse_index(vec.get_feature_names())
    app.logger.debug("All but SVD")
    svdDictionary[course] = np.linalg.svd(vecArr.T) #svd on tfidf documents
    app.logger.debug("SVD Complete")

app.logger.debug("End Vectorizer")
