import re
import numpy as np
import pickle
from app.utils import vectorizer as vecPy
from app.utils import toke

tokenize_method = toke.tokenize_SpaCy

flatten = lambda l: [item for sublist in l for item in sublist]

def get_pos(query):
    pos = re.findall("\+'(.*?)'",query)
    pos = np.array(pos).flatten()
    pos = list(map(tokenize_method, pos))
    pos = sorted(list(set(flatten(pos))))
    return pos

def get_neg(query):
    neg = re.findall("\-'(.*?)'",query)
    neg = np.array(neg).flatten()
    neg = list(map(tokenize_method, neg))
    neg = sorted(list(set(flatten(neg))))
    return neg

def get_mult(query):
    #includes exponent
    mult = re.findall("'[^']+'\^[0-9]+", query)
    exps = list(map(lambda t: int(re.findall("\^([0-9]+)", t)[0]), mult))
    words = list(map(lambda t: re.findall("'([^']+)'\^", t)[0], mult))
    m = {}
    for word, exp in zip(words, exps):
        for w in tokenize_method(word):
            if (w in m and m[w] < exp) or (w not in m):
                m[w] = exp
    #if two words are the exact same, uses greater
    return sorted(list(m.keys())), m

def remove(query):
    #remove +/-
    query = re.sub("[\+\-]'.*?'", ' ', query)
    #remove exp
    query = re.sub("'[^']+'\^[0-9]+", ' ', query)
    return query

def get_all_tokens(query):
    pos = get_pos(query)
    neg = get_neg(query)
    mult, m = get_mult(query)
    query = remove(query)

    other_tokens = tokenize_method(query)
    all_tokens = pos + mult + other_tokens
    all_tokens = " ".join(all_tokens)
    return all_tokens

def create_matrix(query_tokens, docs):
    mat = np.zeros((len(query_tokens), len(docs)))
    for col_id, tokens in enumerate(docs): #col
        for row_id, word in enumerate(query_tokens): #row
            mat[row_id, col_id] = tokens.count(word)
    return mat

def bool_vec(pos_mat, neg_mat, mult_tokens, mult_mat, m, len_docs):
    pos_idx = []
    neg_idx = []
    mult_idx = []
    if pos_mat != []:
        pos_bool = np.prod(pos_mat, axis=0)
        pos_idx = np.where(pos_bool > 0, 1, 0)
    if neg_mat != []:
        neg_bool = np.sum(neg_mat, axis=0)
        neg_idx = np.where(neg_bool == 0, 1, 0)
    if mult_mat != []:
        for idx, word in enumerate(mult_tokens):
            mult_mat[idx] *= m[word]
        mult_idx = np.sum(mult_mat, axis=0)
    result = np.ones(len_docs)
    if pos_idx != []:
        result *= pos_idx
    if neg_idx != []:
        result *= neg_idx
    if mult_idx != []:
        result *= mult_idx

    return result



def boolean(query, course):
    pos = get_pos(query)
    neg = get_neg(query)
    mult, m = get_mult(query)
    # query = remove(query)
    # all_tokens = get_all_tokens(query, pos, neg, mult)

    #z = pickle.load(open("piazza_data_preprocessed.p","rb" ))
    z = vecPy.tokenized_dict[course]
    pos_mat = []
    if len(pos) > 0:
        pos_mat = create_matrix(pos, z)
    neg_mat = []
    if len(neg) > 0:
        neg_mat = create_matrix(neg, z)
    mult_mat = []
    if len(mult):
        mult_mat = create_matrix(mult, z)
    #tokens is in order of rows in matrix
    #doc_ids is in order of columns in matrix
    bool_sim = bool_vec(pos_mat, neg_mat, mult, mult_mat, m, len(z))
    return bool_sim

# query = "+'cumulative'"
# run(query)

