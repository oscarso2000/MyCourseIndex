import os
from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory, jsonify
#from db_setup import init_db, db_session
from urllib.parse import unquote
from piazza_api import Piazza
from app.auth import user_jwt_required, get_name, get_claims
import logging
import html2text


app = Flask(__name__, template_folder="../client/build", static_folder="../client/build/static")

if os.environ.get("deployment", False):
    app.config.from_pyfile('/etc/cs4300-volume-cfg/cs4300app.cfg')
else:
    app.config.from_pyfile(os.path.join(os.path.join(os.getcwd(), "secrets"), "cs4300app.cfg"))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

from app.utils.logging_format import CustomFormatter
gunicorn_logger = logging.getLogger('gunicorn.error')
for handler in gunicorn_logger.handlers:
    handler.setFormatter(CustomFormatter())
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

app.logger.critical("BEFORE IMPORTS")
from app.search.similarity import *
from app.search.boolean_search import *
import app.utils.vectorizer as vecPy
import app.utils.split_vectorizer as vecPySplit
app.logger.critical("AFTER IMPORTS")

p = Piazza()
p.user_login(email=app.config["PIAZZA_USER"], password=app.config["PIAZZA_PASS"])
coursePiazzaIDDict = {
    "CS 4300": app.config["PIAZZA_CS4300_NID"],
    # "INFO 1998": app.config["PIAZZA_INFO1998_NID"]
}

coursePiazzaDict = {
    "CS 4300": p.course(app.config["PIAZZA_CS4300_NID"]),
    # "INFO 1998": p.course(app.config["PIAZZA_INFO1998_NID"])
}


@app.route("/auth", methods=["POST"])
def auth():
    # app.logger.debug("Starting Auth")
    # access_token = request.get_json()["token"]
    # # app.logger.debug("My Token is: {}".format(access_token))
    # app.logger.critical("Should I have access? {}".format(user_jwt_required(access_token, app.config["APP_ID"])))
    # if user_jwt_required(access_token, app.config["APP_ID"]):
    #     return "OK"
    # else:
    #     return "NO"
    return "OK"


@app.route("/whoami", methods=["POST"])
def whoami():
    access_token = request.get_json()["token"]
    # app.logger.debug("My Token is: {}".format(access_token))
    name = get_name(access_token, app.config["APP_ID"])
    return name

@app.route('/search', methods=["POST"])
def search_results():
    access_token = request.get_json()["token"]
    if user_jwt_required(access_token, app.config["APP_ID"]):
        query = unquote(request.get_json()["query"])
        app.logger.info("User queried: {}".format(query))
        #courseSelection = request.args.get("courseSelection")
        courseSelection = "CS 4300"

        #search selection: Default(both),Piazza only, Resource only 
        # [Default, Piazza, Resource]
        
        searchSelection = request.get_json()["search"]
        # searchSelection = "Default"
        
        # if searchSelection == "Default":
        #regular cosine similarity (start commenting out here)
        updated_query = get_all_tokens(query)
        cosine_results= cosineSim(updated_query, vecPy.docVecDictionary , courseSelection, vecPy.courseRevsereIndexDictionary)
        boolean_results= boolean(query, courseSelection)
        svd_results= LSI_SVD(updated_query, vecPy.docVecDictionary, courseSelection, vecPy.courseRevsereIndexDictionary, vecPy.svdDictionary)
    
            
        # finalresults = results #np.multiply(results,vecPy.sourceDictionary[courseSelection])
        if (len(cosine_results) == 0 or len(svd_results) == 0):
            return jsonify([])
        finalresults = np.add(np.multiply(svd_results,boolean_results),np.multiply(cosine_results,boolean_results))
        results_filter = (finalresults > 0.1)
        n= 50 #top x highest

        if len(finalresults) == 0:
            return jsonify([])
        
        reverseList = (-finalresults).argsort() #[:n]
        reverseList_filter = results_filter[reverseList]
        
        n = min(sum(reverseList_filter), n)

        for item, score in zip(vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter], finalresults[reverseList][reverseList_filter]):
            item["score"] = score

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
                return jsonify(vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()[:n])

            else:
                modified_results = list(filter(lambda x: x["type"] != "Piazza", vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()))
                if len(modified_results) == 0:
                    return jsonify([])
                n = min(n, len(modified_results))
                return jsonify(modified_results[:n])   
    
        return jsonify(vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()[:n])
        
    else:
        return "Not Authorized"

@app.route("/courses", methods=["POST"])
def get_user_courses():
    access_token = request.get_json()["token"]
    claims = get_claims(access_token, app.config["APP_ID"])
    if claims["scope"] == "Unauthorized":
        return jsonify([])
    else:
        return jsonify([app.config["COURSE_MAPPING"].get(claim,"") for claim in claims["scope"]])

@app.route("/folders", methods = ["POST"])
def getFolders():
    courseSelection = "CS 4300"
    # searchSelection = request.get_json()["courseSelection"]
    app.logger.critical("{}".format(vecPy.foldersDictionary[courseSelection]))
    return jsonify(vecPy.foldersDictionary[courseSelection])

@app.route("/tokeVerify", methods=["POST"])
def tokeVerify():
    access_token = request.get_json()["token"]
    course = request.get_json()["courseName"]
    their_token = request.get_json()["piazzaToken"]

    claims = get_claims(access_token, app.config["APP_ID"])
    if claims["scope"] == "Unauthorized":
        return "NO"
    else:
        auth_courses = [app.config["COURSE_MAPPING"].get(claim,{"courseName": ""}).get("courseName") for claim in claims["scope"]]
    print("HELLOR: {}".format(course not in auth_courses))
    if course not in auth_courses:
        return "NO"
    h = html2text.HTML2Text()
    h.ignore_links = True
    parsed_piazza = h.handle(coursePiazzaDict[course].get_post(app.config["PIAZZA_" +  course.replace(" ", "") + "_TOKEN_POST"])["history"][0]["content"])
    split_piazza = parsed_piazza.split("\n")
    piazza_token = split_piazza[0]

    return "OK" if piazza_token == their_token else "NO"


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
