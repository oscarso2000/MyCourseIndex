import os
from flask import Flask, render_template, request, redirect, flash
#from db_setup import init_db, db_session
from forms import SearchForm

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.secret_key = 'insert AWS key'


@app.route('/', methods=['GET', 'POST'])
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
