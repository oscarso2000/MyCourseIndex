from pipeline import Pipeline
import boto3
import os
import io
import json
from flask import Flask
import logging
app = Flask(__name__)

key = app.config["AWS_ACCESS"]
secret = app.config["AWS_SECRET"]

# P03Data.json
s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret)
s3.download_file('cs4300-data-models', 'P03Data_mod_concepts.json', 'P03Data.json')
app.logger.debug("Data downloaded")

# S3 JSON Format:
# { "CS4300": {"Piazza": {PostID: content, PostID2: content2}, "Textbook": {DocId: content, DocID2: content2} } }
with open("P03Data.json") as f:
    fromS3 = json.load(f)


courseTextbookDocs = {}
courseContextDocs = {}

for course in fromS3:
    rawDocs = []
    contextDocs = []
    for source in fromS3[course]:
        if source == "Textbook":
            for content in fromS3[course][source]:
                rawDocs.append(fromS3[course][source][content])
                # filestring = convert_pdf_to_string(filepath)
                contextDocs.append(Pipeline.convert_string_to_context(fromS3[course][source][content], 3)) #length -> context length in sentences
    courseTextbookDocs[course] = rawDocs
    courseContextDocs[course] = contextDocs




