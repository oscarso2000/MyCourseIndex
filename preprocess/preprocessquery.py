import preprocessutils
import re
import numpy as np
import pickle

tokenize_method = preprocessutils.tokenize_SpaCy

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

def get_all_tokens(query, pos, neg, mult):
    other_tokens = tokenize_method(query)
    all_tokens = list(set(list(pos) + list(neg) + mult + other_tokens))
    regex = re.compile("[^\s]+")
    all_tokens = sorted(list(filter(regex.match, all_tokens)))
    return all_tokens

def create_matrix(tokens, docs):
    len_docs = 0
    for t in docs:
        len_docs += len(docs[t])
    len_toks = len(tokens)
    mat = np.zeros((len_toks, len_docs))
    doc_ids = []
    for t, post_ids in docs.items():
        doc_ids += post_ids
        for num_tok, tok in enumerate(tokens):
            for num_post, (post_id, counter) in enumerate(post_ids.items()):
                if tok in counter:
                    mat[num_tok, num_post] = counter[tok]
    return mat, tokens, doc_ids

def bool_vec(pos_mat, neg_mat, mult_tokens, mult_mat, m):
    pos_bool = np.prod(pos_mat, axis=0)
    pos_idx = np.where(pos_bool > 0, 1, 0)

    neg_bool = np.sum(neg_mat, axis=0)
    neg_idx = np.where(neg_bool == 0, 1, 0)

    for idx, word in enumerate(mult_tokens):
        mult_mat[idx] *= m[word]

    mult_idx = np.sum(mult_mat, axis=0)

    return pos_idx * neg_idx * mult_idx



def run(query):
    pos = get_pos(query)
    neg = get_neg(query)
    mult, m = get_mult(query)
    query = remove(query)
    all_tokens = get_all_tokens(query, pos, neg, mult)

    z = pickle.load(open("piazza_data_preprocessed.p","rb" ))

    #matrix, row_ids, col_ids
    mat, tokens, doc_ids = create_matrix(all_tokens, z)
    pos_mat, pos_tokens, doc_ids = create_matrix(pos, z)
    neg_mat, neg_tokens, doc_ids = create_matrix(neg, z)
    mult_mat, mult_tokens, doc_ids = create_matrix(mult, z)
    #tokens is in order of rows in matrix
    #doc_ids is in order of columns in matrix
    print(bool_vec(pos_mat, neg_mat, mult_tokens, mult_mat, m))

query = "+'cumulative' +'system discount' -'football' 'score'^3 'unprecidented'^3 'scores'^4 'score'^2"
run(query)

