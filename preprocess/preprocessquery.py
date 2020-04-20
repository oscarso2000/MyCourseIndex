import preprocessutils
import re
import numpy as np

tokenize_method = preprocessutils.tokenize_SpaCy
query = "-'alice bleh' loves the +'sun' '10/8/2020 home '^3 homework +'hello' 'sunshine'^2 'sunshine'^3"

def get_pos(query):
    pos = re.findall("\+'(.*?)'",query)
    pos = np.array(pos).flatten()
    return pos

def get_neg(query):
    neg = re.findall("\-'(.*?)'",query)
    neg = np.array(neg).flatten()
    return neg

def get_mult(query):
    #includes exponent
    mult = re.findall("'[^']+'\^[0-9]+", query)
    exps = list(map(lambda t: int(re.findall("\^([0-9]+)", t)[0]), mult))
    words = list(map(lambda t: re.findall("'([^']+)'\^", t)[0], mult))
    #if two words are the exact same, uses last exponent
    m = dict(zip(words, exps))
    return words, m

def remove(query):
    #remove +/-
    query = re.sub("[\+\-]'.*?'", ' ', query)
    #remove exp
    query = re.sub("'[^']+'\^[0-9]+", ' ', query)
    return query

def get_all_tokens(query, pos, neg, mult):
    other_tokens = tokenize_method(query)
    all_tokens = list(set(list(pos) + list(neg) + mult + other_tokens))
    regex = re.compile("[^\s]+")
    all_tokens = list(filter(regex.match, all_tokens))
    return all_tokens

pos = get_pos(query)
neg = get_neg(query)
mult, m = get_mult(query)
query = remove(query)
all_tokens = get_all_tokens(query, pos, neg, mult)