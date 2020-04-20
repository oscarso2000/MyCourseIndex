import os
from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory, jsonify
#from db_setup import init_db, db_session
from urllib.parse import unquote
from piazza_api import Piazza
from app.auth import user_jwt_required, get_name
from app.search.similarity import *
import app.utils
import app.utils.vectorizer as vecPy
import logging
import html2text


app = Flask(__name__, template_folder="../client/build", static_folder="../client/build/static")
app.logger.setLevel(logging.DEBUG)

if os.environ.get("deployment", False):
    app.config.from_pyfile('/etc/cs4300-volume-cfg/cs4300app.cfg')
else:
    app.config.from_pyfile(os.path.join(os.path.join(os.getcwd(), "secrets"), "cs4300app.cfg"))

p = Piazza()
p.user_login(email=app.config["PIAZZA_USER"], password=app.config["PIAZZA_PASS"])
coursePiazzaIDDict = {
    "CS 4300": app.config["PIAZZA_CS4300_NID"]
}

coursePiazzaDict = {
    "CS 4300": p.course(app.config["PIAZZA_CS4300_NID"])
}


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

@app.route('/search', methods=["POST"])
def search_results():
    access_token = request.get_json()["token"]
    if user_jwt_required(access_token, app.config["APP_ID"], app.logger):
        query = unquote(request.get_json()["query"])
        app.logger.info("User queried: {}".format(query))
        #courseSelection = request.args.get("courseSelection")
        courseSelection = "CS 4300"
        results = cosineSim(query, vecPy.docVecDictionary , courseSelection, app.logger)
        n = 25 #top x highest
        
        #source Dictionary 0.2 for resources, 1 for piazza (weighting)
        finalresults = results #np.multiply(results,vecPy.sourceDictionary[courseSelection])
        
        reverseList = (-finalresults).argsort()[:n]

        if courseSelection == "CS 4300":
            h = html2text.HTML2Text()
            h.ignore_links = True
            parsed_piazza = h.handle(coursePiazzaDict["CS 4300"].get_post(app.config["PIAZZA_CS4300_TOKEN_POST"])["history"][0]["content"])
            split_piazza = parsed_piazza.split("\n")
            piazza_token = split_piazza[0]
            our_token = app.config["PIAZZA_CS4300_TOKEN"]
            keep_piazza = (piazza_token == our_token)

            # app.logger.info("Parsed Piazza: {}".format(repr(parsed_piazza)))
            # app.logger.info("Split Piazza: {}".format(repr(split_piazza)))
            # app.logger.info("Piazza Response: {}".format(repr(piazza_token)))
            # app.logger.info("Our token is: {}".format(repr(our_token)))
            # app.logger.info("Keeping Piazza? {}".format(keep_piazza))
            
            if keep_piazza:
                return jsonify(vecPy.courseDocDictionary[courseSelection][reverseList].tolist())
            else:
                return jsonify(list(filter(lambda x: x["type"] != "Piazza", vecPy.courseDocDictionary[courseSelection][reverseList].tolist())))
        
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
