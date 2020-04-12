import os
from flask import Flask, render_template, request, redirect, flash, url_for
#from db_setup import init_db, db_session
from app.forms import SearchForm
from app.auth import user_jwt_required
from flask_oidc import OpenIDConnect

import logging
import os
from flask import send_from_directory

app = Flask(__name__, template_folder="../client/build", static_folder="../client/build/static")
app.logger.setLevel(logging.DEBUG)
app.config.from_pyfile('/etc/cs4300-volume-cfg/cs4300app.cfg')
# app.config.from_pyfile(os.path.join(os.path.join(os.getcwd(), "secrets"), "cs4300app.cfg"))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.secret_key = 'insert AWS key'

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# oidc = OpenIDConnect(app)

@app.route('/myfavicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'myfavicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET', 'POST'])
# @oidc.require_login
def index():
    return render_template("index.html")
    # access_token = oidc.get_access_token()
    # app.logger.debug(access_token)
    # if not user_jwt_required(access_token, app.config["APP_ID"], app.logger):
    #     return render_template("404.html")
    # search = SearchForm(request.form)
    # if request.method == 'POST':
    #     return search_results(search)
    # return render_template('main.html', form=search)

@app.route('/oidc/callback')
def oidc_callback():
    return redirect(url_for("index"))


@app.route("/auth", methods=["POST"])
def auth():
    # app.logger.debug("Starting Auth")
    access_token = request.get_json()["token"]
    # app.logger.debug("My Token is: {}".format(access_token))
    app.logger.debug("Should I have access? {}".format(user_jwt_required(access_token, app.config["APP_ID"], app.logger)))
    if user_jwt_required(access_token, app.config["APP_ID"], app.logger):
        return "OK"
    else:
        return "NO"


@app.route('/results')
def search_results(search):
    # results here will take in search, 
    # query database, and use IR stuff like 
    # cosine similarity and other stuff to 
    # gain final results array. 
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        return redirect('/')
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
