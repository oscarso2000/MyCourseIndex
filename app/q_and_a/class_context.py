from app.q_and_a.pipeline import convert_string_to_context
import boto3
import os
import io
import json
from flask import Flask
import logging
app = Flask(__name__)

# Retrieve config information from cs4300app.cfg file
if os.environ.get("deployment", False):
    app.config.from_pyfile("/etc/cs4300-volume-cfg/cs4300app.cfg")
else:
    app.config.from_pyfile(os.path.join(
        os.path.join(os.getcwd(), "secrets"), "cs4300app.cfg"))

key = app.config["AWS_ACCESS"]
secret = app.config["AWS_SECRET"]

# P03Data.json
s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret)
s3.download_file('cs4300-data-models', 'P03Data_mod_concepts.json', 'P03Data.json')
app.logger.critical("Data downloaded")

# S3 JSON Format:
# { "CS4300": {"Piazza": {PostID: content, PostID2: content2}, "Textbook": {DocId: content, DocID2: content2} } }
with open("P03Data.json") as f:
    fromS3 = json.load(f)


courseTextbookDocs = {}
courseContextDocs = {}

for course in fromS3:
    app.logger.critical(course)
    rawDocs = []
    contextDocs = []
    for source in fromS3[course]:
        app.logger.critical(source)
        if source == "Resource":
            for content in fromS3[course][source]:
                app.logger.critical(content)
                rawDocs.append(fromS3[course][source][content]["raw"])
                # filestring = convert_pdf_to_string(filepath)
                contextDocs.append(convert_string_to_context(fromS3[course][source][content]["raw"], 3)) #length -> context length in sentences
    courseTextbookDocs[course] = rawDocs
    courseContextDocs[course] = contextDocs
    # app.logger.critical(rawDocs)
    app.logger.critical(courseContextDocs["CS 4300"][1][1])
    app.logger.critical(courseContextDocs["CS 4300"][2][0])





