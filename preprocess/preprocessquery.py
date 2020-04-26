import preprocessutils
import re
import numpy as np
import pickle

tokenize_method = preprocessutils.tokenize_SpaCy
query = "-'gain' +'cumulative' 'score'^3"

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
    return list(m.keys()), m

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

z = pickle.load(open("piazza_data_preprocessed.p","rb" ))

def create_matrix(tokens, docs):
    len_docs = 0
    for t in z:
        len_docs += len(z[t])
    len_toks = len(tokens)
    mat = np.zeros((len_toks, len_docs))
    doc_ids = []
    for t, post_ids in z.items():
        doc_ids += post_ids
        for num_tok, tok in enumerate(tokens):
            for num_post, (post_id, counter) in enumerate(post_ids.items()):
                if tok in counter:
                    mat[num_tok, num_post] = counter[tok]
    return mat, tokens, doc_ids

            
#matrix, row_ids, col_ids
mat, tokens, doc_ids = create_matrix(all_tokens, z)
pos_mat, pos_tokens, doc_ids = create_matrix(pos, z)
neg_mat, neg_tokens, doc_ids = create_matrix(neg, z)
mult_mat, mult_tokens, doc_ids = create_matrix(mult, z)
#tokens is in order of rows in matrix
#doc_ids is in order of columns in matrix