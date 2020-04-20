import os
from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory, jsonify
#from db_setup import init_db, db_session
from app.auth import user_jwt_required, get_name
from app.search.similarity import *
import app.utils
import app.utils.vectorizer as vecPy
import logging


app = Flask(__name__, template_folder="../client/build", static_folder="../client/build/static")
app.logger.setLevel(logging.DEBUG)

if os.environ.get("deployment", False):
    app.config.from_pyfile('/etc/cs4300-volume-cfg/cs4300app.cfg')
else:
    app.config.from_pyfile(os.path.join(os.path.join(os.getcwd(), "secrets"), "cs4300app.cfg"))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)




@app.route("/auth", methods=["POST"])
def auth():
    # app.logger.debug("Starting Auth")
    access_token = request.get_json()["token"]
    # app.logger.debug("My Token is: {}".format(access_token))
    app.logger.critical("Should I have access? {}".format(user_jwt_required(access_token, app.config["APP_ID"], app.logger)))
    if user_jwt_required(access_token, app.config["APP_ID"], app.logger):
        return "OK"
    else:
        return "NO"


@app.route("/whoami", methods=["POST"])
def whoami():
    access_token = request.get_json()["token"]
    # app.logger.debug("My Token is: {}".format(access_token))
    name = get_name(access_token, app.config["APP_ID"], app.logger)
    return name

@app.route("/search", methods=["POST"])
def search():
    print(request.get_json())
    query = request.get_json()['query']
    print(query)
    return '[{"folders": ["exam"], "nr": 532, "data": {"embed_links": []}, "created": "2020-03-09T21:50:43Z", "bucket_order": 3, "no_answer_followup": 0, "change_log": [{"anon": "stud", "data": "k7l021ycvg65bl", "type": "create", "when": "2020-03-09T21:50:43Z", "uid_a": "a_0"}, {"anon": "stud", "data": "k7l04umombn6pr", "to": "k7l021yaje65bk", "type": "s_answer", "when": "2020-03-09T21:52:54Z", "uid_a": "a_1"}, {"anon": "stud", "to": "k7l021yaje65bk", "type": "followup", "when": "2020-03-09T21:55:29Z", "uid_a": "a_0"}, {"anon": "stud", "data": "k7l0c43zz4g26n", "type": "s_answer_update", "when": "2020-03-09T21:58:33Z", "uid_a": "a_1"}, {"anon": "stud", "to": "k7l021yaje65bk", "type": "feedback", "when": "2020-03-09T22:00:05Z", "uid_a": "a_2"}, {"anon": "stud", "data": "k7l0f76z7496f5", "type": "s_answer_update", "when": "2020-03-09T22:00:57Z", "uid_a": "a_1"}], "bucket_name": "Today", "history": [{"anon": "stud", "uid_a": "a_0", "subject": "Explaining Precision-Recall Plot", "created": "2020-03-09T21:50:43Z", "content": "<p><img src=\\"/redirect/s3?bucket=uploads&amp;prefix=attach%2Fk5h3t0fy1gm5vv%2Fis7ndxn611v674%2Fk7l014piz5pc%2FScreen_Shot_20200309_at_5.49.24_PM.png\\" alt=\\"\\" /></p>\\n<p></p>\\n<p>Would anyone mind explaining how to read the Precision-Recall graph and what this exactly shows about Systems 1, 2 and 3?</p>"}], "type": "question", "tags": ["exam", "student"], "tag_good": [], "unique_views": 113, "children": [{"folders": [], "data": {"embed_links": []}, "children": [], "created": "2020-03-09T21:52:54Z", "bucket_order": 3, "tag_endorse": [{"role": "ta", "name": "Andrew Xu", "endorser": {}, "admin": true, "photo": null, "id": "is9g43pyqch7k2", "photo_url": null, "published": true, "us": false, "facebook_id": null}, {"role": "student", "name": "Emily", "endorser": {}, "admin": false, "photo": null, "id": "is7kxro2wi53b7", "photo_url": null, "published": true, "us": false, "facebook_id": null}, {"role": "student", "name": "Amrit Amar", "endorser": {"jzob4kisizv2n0": 1574103584}, "admin": false, "photo": null, "id": "is54wjorks21mx", "photo_url": null, "us": false, "facebook_id": null}], "bucket_name": "Today", "id": "k7l04umlju96pq", "history": [{"anon": "stud", "uid_a": "a_1", "subject": "", "created": "2020-03-09T22:00:57Z", "content": "<p><img src=\\"https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Precisionrecall.svg/800px-Precisionrecall.svg.png\\" alt=\\"\\" width=\\"301\\" height=\\"547\\" /></p>\\n<p>I personally find this graphic very helpful in explaining precision and recall.</p>\\n<p>Precision is how many of the selected items are actually relevant, and recall is how many of the relevant items have been selected.</p>\\n<p>How I understand it is: Low recall and high precision means few items have been selected, but they are all or mostly relevant. High recall and high precision means that many items have been selected and are mostly relevant. Low recall and low precision means that there are a lot of irrelevant items selected. High recall and low precision means that many relevant items have been selected, but many irrelevant items have also been selected.</p>"}, {"anon": "stud", "uid_a": "a_1", "subject": "", "created": "2020-03-09T21:58:33Z", "content": "<p><img src=\\"https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Precisionrecall.svg/800px-Precisionrecall.svg.png\\" alt=\\"\\" width=\\"301\\" height=\\"547\\" /></p>\\n<p>I personally find this graphic very helpful in explaining precision and recall.</p>\\n<p>Precision is how many of the selected items are actually relevant, and recall is how many of the relevant items have been selected.</p>\\n<p>How I understand it is: Low recall and high precision means few items have been selected, but they are all or mostly relevant. Low recall and low precision means that few items have been selected and are mostly irrelevant. High recall and high precision means that many items have been selected and are mostly relevant. High recall and low precision means that multiple items have been selected and there&#39;s a mix of relevant and irrelevant items.</p>"}, {"anon": "stud", "uid_a": "a_1", "subject": "", "created": "2020-03-09T21:52:54Z", "content": "<p><img src=\\"https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Precisionrecall.svg/800px-Precisionrecall.svg.png\\" alt=\\"\\" width=\\"301\\" height=\\"547\\" /></p>\\n<p>I personally find this graphic very helpful in explaining precision and recall.</p>"}], "type": "s_answer", "tag_endorse_arr": ["is9g43pyqch7k2", "is7kxro2wi53b7", "is54wjorks21mx"], "config": {}, "is_tag_endorse": false}, {"anon": "stud", "folders": [], "data": {"embed_links": null}, "no_upvotes": 0, "subject": "<p>I understand the concept behind precision and recall but am having trouble understanding the relationship between the two when graphed like above.\\u00a0</p>", "created": "2020-03-09T21:55:29Z", "bucket_order": 4, "bucket_name": "Yesterday", "type": "followup", "tag_good": [], "uid_a": "a_0", "children": [{"anon": "stud", "folders": [], "data": {"embed_links": null}, "subject": "<p>Typically, when precision-recall curves\\u00a0have higher levels of precision at lower levels of recall, that means the system prefers precision over recall (such as Google since they want the first few results to be relevant because most users just click on the first link). When a precision-recall curve has higher levels of precision at higher levels of recall, that means that the system prefers recall over precision (such as a system a researcher would\\u00a0want to use to get as many documents as possible that might be related to their topic of interest)\\u00a0</p>", "created": "2020-03-09T22:00:05Z", "bucket_order": 4, "bucket_name": "Yesterday", "type": "feedback", "tag_good": [{"role": "student", "name": "Theodore", "endorser": {}, "admin": false, "photo": null, "id": "is7ndxn611v674", "photo_url": null, "published": true, "us": false, "facebook_id": null}, {"role": "professor", "name": "Cristian Danescu-Niculescu-Mizil", "endorser": {}, "admin": true, "photo": null, "id": "gsam27wdzbb", "photo_url": null, "us": false, "facebook_id": null}, {"role": "student", "name": "Emily", "endorser": {}, "admin": false, "photo": null, "id": "is7kxro2wi53b7", "photo_url": null, "published": true, "us": false, "facebook_id": null}, {"role": "student", "name": "Andre Lee", "endorser": {}, "admin": false, "photo": null, "id": "is67u38ddyn29b", "photo_url": null, "published": true, "us": false, "facebook_id": null}], "uid_a": "a_2", "children": [], "tag_good_arr": ["is7ndxn611v674", "gsam27wdzbb", "is7kxro2wi53b7", "is67u38ddyn29b"], "id": "k7l0e32jg2m67a", "d-bucket": "Yesterday", "updated": "2020-03-09T22:00:05Z", "config": {}}], "tag_good_arr": [], "no_answer": 0, "id": "k7l086khi5o5fb", "d-bucket": "Yesterday", "updated": "2020-03-09T21:55:29Z", "config": {}}], "tag_good_arr": [], "no_answer": 0, "id": "k7l021yaje65bk", "config": {"seen": {"111": 2, "398": 1, "431": 5, "399": 4, "349": 0, "480": 6, "470": 7, "65": 3}}, "status": "active", "request_instructor": 0, "request_instructor_me": false, "bookmarked": 3, "num_favorites": 1, "my_favorite": false, "is_bookmarked": false, "is_tag_good": false, "q_edits": [], "i_edits": [], "s_edits": [], "t": 1587229410185, "default_anonymity": "no"}]'

@app.route('/results')
def search_results():
    access_token = request.get_json()["token"]

    if user_jwt_required(access_token, app.config["APP_ID"], app.logger):

        query = request.args.get("query")
        app.logger.info("User queried: {}".format(query))
        #courseSelection = request.args.get("courseSelection")
        courseSelection = "CS 4300"
        results = cosineSim(query, vecPy.docVecDictionary , courseSelection)
        n = 50 #top x highest
        
        reverseList = (-results).argsort()[:n]

        return jsonify(vecPy.courseDocDictionary[courseSelection][reverseList].tolist())
    else:
        return "Not Authorized"


@app.route("/manifest.json")
def manifest():
    return send_from_directory(os.path.join(app.root_path, "../client/build"),'manifest.json')


@app.route('/ColorMCIfavicon.ico')
def ColorMCIfavicon():
    return send_from_directory(os.path.join(app.root_path, "static"),"ColorMCIfavicon.ico")


@app.route('/oidc/callback', methods=['GET'])
def oidc_callback():
    return redirect(url_for("index"))


@app.route('/', methods=['GET'], defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html")
    


# application.add_api('spec.yml')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
