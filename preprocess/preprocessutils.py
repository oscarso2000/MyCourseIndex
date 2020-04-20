import re
import json
from glob import glob
import os
from io import StringIO
from itertools import groupby
import html2text
import pickle

import numpy as np
import bs4
from IPython import get_ipython
# get_ipython().run_line_magic('matplotlib', 'inline')
# import matplotlib.pyplot as plt

import spacy
sp = spacy.load('en_core_web_sm')

from collections import Counter


import sys
# Ensure that your kernel is using Python3
assert sys.version_info.major == 3


with open('../sample_data.json', 'r') as f:
    data_dict = json.load(f)['data']


h = html2text.HTML2Text()
h.ignore_links = True


# data_dict is a list of 100 posts
# 
# each post is a dictionary with the following keys:
# 
#  'folders', 'nr', 'data', 'created', 'bucket_order', 'no_answer_followup', 
#  'change_log', 'bucket_name', 'history', 'type', 'tags', 'tag_good', 'unique_views', 
#  'children', 'tag_good_arr', 'id', 'config', 'status', 'request_instructor', 
#  'request_instructor_me', 'bookmarked', 'num_favorites', 'my_favorite', 'is_bookmarked', 
#  'is_tag_good', 'q_edits', 'i_edits', 's_edits', 't', 'default_anonymity'
# 
# ADD MEANING OF EACH OF THE KEYS ABOVE
#  nr - unique post number used in url
#  nr = post_id
# 
# Converting to a super simple data structure with very little remaining info.
# Here is the layout of the data structure:
# 
# {post_id:
# 
#    folders: [],
#    
#    subject:"",
#
#    followups:"",
#
#    question: "",
#    
#    s_answer: "",
#    
#    i_answer: "" }

simple_dict = {}
all_folders = Counter()
processed_simple_dict = {}
all_folders_lst = []


for post in data_dict:
    post_id = post['nr']
    folders = post['folders']
    subject = post['history'][0]['subject']
    question = post['history'][0]['content']
    s_answer = ""
    i_answer = ""
    followups = ""
    all_folders_lst.extend(folders)
    for answer in post['children']:
        if answer['type'] == "i_answer":
            i_answer = answer['history'][0]['content']
        elif answer['type'] == "s_answer":
            s_answer = answer['history'][0]['content']
        elif answer['type'] == "followup": 
            followups = answer['subject']
            for fb in answer['children']:
                followups += fb['subject']
    simple_dict[post_id] = {"folders": folders, "subject":subject,"question": question, "s_answer": s_answer, "i_answer": i_answer, "followups":followups}
    processed_simple_dict[post_id] = {"folders": folders,"subject":h.handle(subject).replace("\n","") ,"question": h.handle(question).replace("\n", ""), 
                            "s_answer": h.handle(s_answer).replace("\n", ""), 
                            "i_answer": h.handle(i_answer).replace("\n", ""),
                            "followups":h.handle(followups).replace("\n","")}
    
all_folders = Counter(all_folders_lst)

# print(h.handle("<p>Hello, <a href='https://www.google.com/earth/'>world</a>!"))
# returns print statement as : Hello, world!


def tokenize_w_numbers(text):
    """Returns a list of words that make up the text.
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Params: {text: String}
    Returns: List
    """
    # YOUR CODE HERE
    text = text.lower()
    x = re.findall("[a-zA-Z0-9]+",text)
    return x
def tokenize_wo_numbers(text):
    """Returns a list of words that make up the text.
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Params: {text: String}
    Returns: List
    """
    # YOUR CODE HERE
    text = text.lower()
    x = re.findall("[a-zA-Z]+",text)
    return x

def tokenize_SpaCy(text):
    """Returns a list of words that make up the text.
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Params: {text: String}
    Returns: List
    """
    text = text.lower()
    tokenized = sp(text)    
    return [w.lemma_ for w in tokenized if not w.is_punct and not w.is_stop]


def tokenize_transcript(tokenize_method,input_transcript):
    """Returns a list of words contained in an entire transcript.
    Params: {tokenize_method: Function (a -> b),
             input_transcript: Tuple}
    Returns: List
    """
    # YOUR CODE HERE
    token_dict = {}
    
    total_tokens = []
    for (k,i) in input_transcript.items():
        token_simpl_dict = {}
        token_simpl_dict['folders'] = i['folders']
        question = tokenize_method(i['question'])
        total_tokens.extend(question)
        token_simpl_dict['question'] = Counter(question)
        i_answer = tokenize_method(i['i_answer'])
        total_tokens.extend(i_answer)
        token_simpl_dict['i_answer'] = Counter(i_answer)
        s_answer = tokenize_method(i['s_answer'])
        total_tokens.extend(s_answer)
        token_simpl_dict['s_answer'] = Counter(s_answer)
        subject = tokenize_method(i['subject'])
        total_tokens.extend(subject)
        token_simpl_dict['subject'] = Counter(subject)
        followups = tokenize_method(i['followups'])
        total_tokens.extend(followups)
        token_simpl_dict['followups'] = Counter(followups)
        token_dict[k] = token_simpl_dict
    return (token_dict, Counter(total_tokens))


(tokenized_spacy_dict, total_tokens_spacy) = tokenize_transcript(tokenize_SpaCy, processed_simple_dict)

(tokenized_num_dict, total_tokens_w_num) = tokenize_transcript(tokenize_w_numbers, processed_simple_dict)

(tokenized_no_num_dict, total_tokens_wo_num) = tokenize_transcript(tokenize_wo_numbers, processed_simple_dict)

main_sample_dict_processed = {"tokenized_num_dict":tokenized_num_dict, "tokenized_no_num_dict":tokenized_no_num_dict, "total_tokens_w_num":total_tokens_w_num, "total_tokens_wo_num":total_tokens_wo_num, "tokenized_spacy_dict":tokenized_spacy_dict, "total_tokens_spacy":total_tokens_spacy}

# main_sample_dict_processed.keys()
# keys are as follows: dict_keys(['tokenized_num_dict', 'tokenized_no_num_dict', 'total_tokens_w_num', 'total_tokens_wo_num', 'tokenized_spacy_dict', 'total_tokens_spacy'])

pickle.dump( main_sample_dict_processed, open( "sample_data_preprocessed.p", "wb" ) )

def build_inverted_index(nrs):
    """ Builds an inverted index from the messages."""
    folders = set()
    result = {}
    for nr, nr_dict in nrs.items():
        folder = nr_dict["folders"]
        for word_freq in [nr_dict["question"], nr_dict["s_answer"], nr_dict["i_answer"]]:
            for word, freq in word_freq.items():
                for fold in folder:
                    if fold not in folders:
                        folders.add(fold)
                    if word in result:
                        if fold in result[word]:
                            result[word][fold] += freq
                        else:
                            result[word][fold] = freq
                    else:
                        result[word] = {fold: freq}
    for word, fold_freq in result.items():
        result[word] = list(fold_freq.items())
    return result, folders

#Note: these defaults don't prune any words
def compute_idf(inv_idx, n_docs, min_df=1, max_df_ratio=1.0):
    """ Compute term IDF values from the inverted index.
    Words that are too frequent or too infrequent get pruned."""
    # YOUR CODE HERE
    idf = {}
    max_df = max_df_ratio * n_docs
    for key, value in inv_idx.items():
        df = len(value)
        if df >= min_df and df <= max_df:
            #don't need +1 in denominator because we won't have any empty lists
            idf[key] = round(np.log2(n_docs / df), 2)
    return idf

# inv_idx, folders = build_inverted_index(tokenized_no_num_dict)
# n_docs = len(folders)
# idf = compute_idf(inv_idx, n_docs)
# idf = {k: v for k, v in sorted(idf.items(), key=lambda item: item[1], reverse=True)}