# This file's (signup_data.py) purpose is to upload the class signup data
# from MyCourseIndex to s3. Specifically, it handles the Piazza class URL,
# the CSV file from the Box link, and the Canvas enrollment process.

import boto3
import os
import json
from flask import Flask
app = Flask(__name__)

# Retrieve config information from cs4300app.cfg file
if os.environ.get("deployment", False):
  app.config.from_pyfile("/etc/cs4300-volume-cfg/cs4300app.cfg")
else:
  app.config.from_pyfile(os.path.join(os.path.join(os.getcwd(), "secrets"), "cs4300app.cfg"))

# Okay, now we can use our key & secret to access the s3 bucket.
key = app.config["AWS_ACCESS"]
secret = app.config["AWS_SECRET"]
s3 = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret)

# # We will be working with this bucket & file for our uploads
# bucket_name = "cs4300-data-models"
# fname = "class-signup-data.json"
# fkey = os.path.splitext(os.path.basename(fname))[0]

# # Uploads a new, empty file just for initialization the first time
# with open(fname, "w") as fp:
#   pass
# s3.upload_file(fname, bucket_name, fkey)

# # Print contents of bucket (for debugging)
# obj_list = s3.list_objects(Bucket=bucket_name)["Contents"]
# # s3.download_file(bucket_name, "key", "file")

# # TODO: Some code here to handle the frontend input form
# # Should have piazza_link, class_name; example:
# class_name = "ECE 3030"
# piazza_link = "https://piazza.com/class/keg4jr6zdp76u7?cid=40"

# # Gets just the class id portion from the link, even if there is junk
# piazza_id = piazza_link.rsplit("/class/", 1)[-1].split("?", 1)[0].split("/", 1)[0]

# # Generates a JSON-formatted dict with class name and piazza ID
# class_info_json = {"class": {"name": class_name, "piazza": piazza_id}}


def add_course(email, course_name, piazza_link, canvas_link, csv):
    # TODO1: preprocess course name info1998 => INFO 1998
    # TODO2: check if csv is correct format
    # TODO3: check canvas link or external website or valid
    # TODO4: check piazza_link is valid
    try:
        s3.downloadFile('mci-prof-form',
                        'class-signup-data.json', 'signupData.json')
        with open('signupData.json', "r") as fp:
            signup_data = json.load(fp)
    except:
        signup_data = {}
    signup_data[course_name] = {"email": email, "course_name": course_name,
                                "piazza_link": piazza_link, "canvas_link": canvas_link, "csv": csv, "is_canvas": True}
    with open('signupData.json', "w") as fp:
        json.dump(signup_data, fp, indent=4)
    s3.upload_file('signupData.json', 'mci-prof-form',
                   'class-signup-data.json')
