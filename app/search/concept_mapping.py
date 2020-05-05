import codecs
import os
from quickumls import QuickUMLS as QuickUCSLS
from flask import Flask
import logging
from app.search.boolean_search import (
    get_pos,
    get_neg,
    get_mult,
    remove
)
app = Flask(__name__)

if os.environ.get("deployment", False):
    app.config.from_pyfile('/etc/cs4300-volume-cfg/cs4300app.cfg')
else:
    app.config.from_pyfile(os.path.join(
        os.path.join(os.getcwd(), "secrets"), "cs4300app.cfg"))

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


os.system("cp -r concept_matching/quickUCSLS concept_matching/quickUCSLS_{}".format(os.getpid()))
app.logger.debug("PID: {}".format(os.getpid()))

concept_matcher = QuickUCSLS("./concept_matching/quickUCSLS_{}".format(os.getpid()), accepted_semtypes={"T{:03d}".format(i) for i in range(1,35)}, threshold=0.5, min_match_length=0)
app.logger.debug("Matcher res: {}".format(concept_matcher.match("cos sim")))
app.logger.debug("Matcher Ready")

def get_preferred_terms():
    preferred_term = dict()
    with codecs.open("./concept_matching/definition_files/MRCONSO.RRF") as f:
        for i, ln in enumerate(f):
            if i < 1:
                continue
            cui, s, _, pref = ln.strip().split("|")
            if pref == "Y":
                preferred_term[cui] = s
    return preferred_term

preferred_term = get_preferred_terms()

def concept_modify_query(query):
    matches = concept_matcher.match(query)
    matches = list(map(lambda x: x[0], matches))
    mod_query = query

    for match in matches:
        ngram = match["ngram"]
        app.logger.debug("ngram: {}".format(ngram))
        concept = match["cui"]
        app.logger.debug("match: {}".format(match))
        term = preferred_term[concept]
        mod_query = mod_query.replace(ngram, term)
    return mod_query


def concept_modify_query_bool(query):
    pos = get_pos(query)
    neg = get_neg(query)
    mult, m = get_mult(query)
    phrases = []
    phrases.extend(pos); phrases.extend(neg); phrases.extend(mult)
    mod_query = query
    app.logger.debug("Phrases {}".format(phrases))
    for word in phrases:
        matches = concept_matcher.match(word)
        matches = list(map(lambda x: x[0], matches))
        for match in matches:
            ngram = match["ngram"]
            concept = match["cui"]
            term = preferred_term[concept]
            mod_query = mod_query.replace(ngram, term)

    app.logger.debug("mod query: {}".format(repr(mod_query)))
    clean_query = remove(mod_query)
    app.logger.debug("clean query: {}".format(repr(clean_query)))

    matches = concept_matcher.match(clean_query)
    matches = list(map(lambda x: x[0], matches))
    app.logger.debug("Matches: {}".format(matches))
    # mod_query = query

    for match in matches:
        ngram = match["ngram"]
        app.logger.debug("ngram: {}".format(ngram))
        concept = match["cui"]
        app.logger.debug("match: {}".format(match))
        term = preferred_term[concept]
        mod_query = mod_query.replace(ngram, term)

    return mod_query
