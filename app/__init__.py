import os
from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory
#from db_setup import init_db, db_session
from app.auth import user_jwt_required, get_name
from app.search.similarity import *
import app.utils
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


@app.route('/results')
def search_results():
    # results here will take in search, 
    # query database, and use IR stuff like 
    # cosine similarity and other stuff to 
    # gain final results array. 
    query = request.args.get("query")
    #course = request.args.get("courseSelection")
    results = cosineSim(query, utils.vectorizer.docVecDictionary , "CS 4300")
    
    #n = request.args.get("numberOfResults")
    n = 50 #top x highest
    
    #INCOMPLETE: TODO NEEDS FIXING UP
    #Return the documents TEXT&ID most highly similar 
    #returns indices of highest n similarity values
    reverseList = (-results).argsort()[:n]
    print(results[reverseList])

    return results
    
    
    # print([documents[x] for x in returnedResults])


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
