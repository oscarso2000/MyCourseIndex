import os
from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory, jsonify
#from db_setup import init_db, db_session
from urllib.parse import unquote
from piazza_api import Piazza
from app.auth import user_jwt_required, get_name
from app.search.similarity import *
from app.search.boolean_search import *
import app.utils
import app.utils.vectorizer as vecPy
import app.utils.split_vectorizer as vecPySplit
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

        #search selection: Default(both),Piazza only, Resource only 
        # [Default, Piazza, Resource]
        #searchSelection = request.args.get("searchSelection")
        searchSelection = "Default"
        
        # if searchSelection == "Default":
        #regular cosine similarity (start commenting out here)
        updated_query = get_all_tokens(query)
        cosine_results, results_filter = cosineSim(updated_query, vecPy.docVecDictionary , courseSelection, app.logger)
        boolean_results, results_filter = run(query, courseSelection)

        n = 25 #top x highest
            
        #source Dictionary 0.2 for resources, 1 for piazza (weighting)
        # finalresults = results #np.multiply(results,vecPy.sourceDictionary[courseSelection])
        if len(cosine_results) == 0:
            return jsonify([])
        finalresults = np.multiply(cosine_results,boolean_results)
        results_filter = (finalresults > 0)

        if len(finalresults) == 0:
            return jsonify([])
        
        reverseList = (-finalresults).argsort() #[:n]
        reverseList_filter = results_filter[reverseList]
        
        n = min(sum(reverseList_filter), n)

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
                if (searchSelection == "Default"):
                    return jsonify(vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()[:n])
                elif (searchSelection == "Piazza"):
                    modified_results = list(filter(lambda x: x["type"] != "Resource", vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()))
                    if len(modified_results) == 0:
                        return jsonify([])
                    n = min(n, len(modified_results))
                    return jsonify(modified_results[:n])   
                elif (searchSelection == "Resource"):
                    modified_results = list(filter(lambda x: x["type"] != "Piazza", vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()))
                    if len(modified_results) == 0:
                        return jsonify([])
                    n = min(n, len(modified_results))
                    return jsonify(modified_results[:n])      
            else:
                if (searchSelection == "Default"):
                    modified_results = list(filter(lambda x: x["type"] != "Piazza", vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()))
                    if len(modified_results) == 0:
                        return jsonify([])
                    n = min(n, len(modified_results))
                    return jsonify(modified_results[:n])   
                elif (searchSelection == "Piazza"):
                    return jsonify([]) 
                elif (searchSelection == "Resource"):
                    modified_results = list(filter(lambda x: x["type"] != "Piazza", vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()))
                    if len(modified_results) == 0:
                        return jsonify([])
                    n = min(n, len(modified_results))
                    return jsonify(modified_results[:n])   
                
        if (searchSelection == "Default"):
            return jsonify(vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()[:n])
        elif (searchSelection == "Piazza"):
            modified_results = list(filter(lambda x: x["type"] != "Resource", vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()))
            if len(modified_results) == 0:
                return jsonify([])
            n = min(n, len(modified_results))
            return jsonify(modified_results[:n])   
        elif (searchSelection == "Resource"):
            modified_results = list(filter(lambda x: x["type"] != "Piazza", vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()))
            if len(modified_results) == 0:
                return jsonify([])
            n = min(n, len(modified_results))
            return jsonify(modified_results[:n])      
        # return jsonify(vecPy.courseDocDictionary[courseSelection][reverseList][reverseList_filter].tolist()[:n])
          
        # else:
        # # #split cosine sim between piazza and resource (or here)
        # # #uses split_vectorizer.py instead
        #     piazza_results, piazza_results_filter, resource_results, resource_results_filter = cosineSimSplit(query, vecPySplit.docVecDictionary , courseSelection)
        #     n = 25
            
        #     if searchSelection == "Piazza":
        #         finalresults = piazza_results
        #         results_filter = piazza_results_filter
        #     elif searchSelection == "Resource":
        #         finalresults = resource_results
        #         results_filter = resource_results_filter
            
        #     if len(finalresults) == 0:
        #         return jsonify([])
            
        #     reverseList = (-finalresults).argsort() #[:n]
        #     reverseList_filter = results_filter[reverseList]

        #     n = min(sum(reverseList_filter), n)

        #     if courseSelection == "CS 4300":
        #         h = html2text.HTML2Text()
        #         h.ignore_links = True
        #         parsed_piazza = h.handle(coursePiazzaDict["CS 4300"].get_post(app.config["PIAZZA_CS4300_TOKEN_POST"])["history"][0]["content"])
        #         split_piazza = parsed_piazza.split("\n")
        #         piazza_token = split_piazza[0]
        #         our_token = app.config["PIAZZA_CS4300_TOKEN"]
        #         keep_piazza = (piazza_token == our_token)
                
        #         if keep_piazza:
        #             return jsonify(vecPySplit.courseDocDictionary[courseSelection][searchSelection][reverseList].tolist()[:n])
        #         else:
        #             modified_results = list(filter(lambda x: x["type"] != "Piazza", vecPySplit.courseDocDictionary[courseSelection][searchSelection][reverseList][reverseList_filter].tolist()))
        #             n = min(n, len(modified_results))
        #             return jsonify(modified_results[:n])     
                
        #     return jsonify(vecPySplit.courseDocDictionary[courseSelection][searchSelection][reverseList][reverseList_filter].tolist()[:n])
          
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
