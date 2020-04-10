import os
from flask import Flask, render_template, request, redirect, flash
#from db_setup import init_db, db_session
from app.forms import SearchForm
from flask_oidc import OpenIDConnect

import os

app = Flask(__name__)
app.config.from_pyfile('/etc/cs4300-volume-cfg/cs4300app.cfg')
# app.config.from_pyfile(os.path.join(os.path.join(os.getcwd(), "secrets"), "cs4300app.cfg"))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.secret_key = 'insert AWS key'

oidc = OpenIDConnect(app)

@app.route('/', methods=['GET', 'POST'])
@oidc.require_login
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('main.html', form=search)


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
