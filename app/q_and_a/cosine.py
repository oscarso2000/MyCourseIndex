import argparse

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import torch
from transformers import (
    BertTokenizer,
    BertForQuestionAnswering,
)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words

import nltk
import os
import string
import numpy as np
import copy
import pandas as pd
import pickle
import re
import math


def convert_pdf_to_string(file_path):

	output_string = StringIO()
	with open(file_path, 'rb') as in_file:
	    parser = PDFParser(in_file)
	    doc = PDFDocument(parser)
	    rsrcmgr = PDFResourceManager()
	    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
	    interpreter = PDFPageInterpreter(rsrcmgr, device)
	    for page in PDFPage.create_pages(doc):
	        interpreter.process_page(page)
	text = output_string.getvalue()
	text = text.replace('\x0c','')
	text = text.replace('\xa0','')
	text = text.replace('\n','')
	text = text.replace('ﬀ', 'ff') # double f's seem to get messed up a lot?
	return(text)

def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")

def stemming(data):
    stemmer= PorterStemmer()
    
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data)
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data) 
    data = remove_stop_words(data)
    return data

def convert_string_to_context(file_string, length):
	context = []
	splits = file_string.split('.')
	rem = len(splits)%length
	iters = int((len(splits) - rem)/length)

	for i in range(iters):
		block = ""
		for j in range(length):
			block += splits[i*length+j] + ". "
		context.append(block)

	if rem > 0:
		block = ""
		for j in range(rem):
			block += splits[(i+1)*length+j] + ". "
		context.append(block)

	return context

def c_freq(word, DF):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c

def process(context):
  dataset = []
  DF = {}
  for i in range(len(context)):
      tokens = word_tokenize(str(preprocess(context[i])))
      dataset.append(tokens)
      for w in tokens:
          try:
              DF[w].add(i)
          except:
              DF[w] = {i}

  for i in DF:
      DF[i] = len(DF[i])

  c = 0
  tf_idf = {}
  N = len(context)
  for i in range(N):    
      tokens = dataset[i]
      counter = Counter(dataset[i])
      words_count = len(dataset[i])
      
      for token in np.unique(tokens): 
          tf = counter[token]/words_count
          df = c_freq(token, DF)
          idf = np.log((N+1)/(df+1))
          
          tf_idf[c, token] = tf*idf
      c += 1
  return tf_idf, DF

def cosine_sim(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
      cos_sim = -1
    else:
      cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim

def gen_vector(tokens, context, total_vocab, DF):

    N = len(context)

    Q = np.zeros(len(total_vocab))
    
    counter = Counter(tokens)
    words_count = len(tokens)

    query_weights = {}
    
    for token in np.unique(tokens):
        
        tf = counter[token]/words_count
        # print("tf :", tf)
        df = c_freq(token, DF)
        # print("df :", df)
        idf = math.log((N+1)/(df+1))
        # print("idf :", idf)
        try:
            ind = total_vocab.index(token)
            Q[ind] = tf*idf
        except:
            pass
    return Q

def cosine_similarity(k, query, context):
    print("Cosine Similarity")
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))
    
    print("\nQuery:", query)
    print("")
    print(tokens)
    
    d_cosines = []

    tf_idf, DF = process(context)
    N = len(context)
    # vectorizing
    total_vocab_size = len(DF)
    total_vocab = [x for x in DF]
    D = np.zeros((N, total_vocab_size))
    for i in tf_idf:
        try:
            ind = total_vocab.index(i[1])
            D[i[0]][ind] = tf_idf[i]
        except:
            pass
    query_vector = gen_vector(tokens, context, total_vocab, DF)
    
    for d in D:
        d_cosines.append(cosine_sim(query_vector, d))
    
    # print(d_cosines)
    s = sorted(d_cosines, reverse=True)
    if d_cosines[0] == -1:
      print("Answer likely not in this document")
    else:
      out = np.array(d_cosines).argsort()[-k:][::-1]
      print("")
      
      # for i in range(k):
      #   print(context[out[i]])
      print(out)

def passed_arguments():
	parser = argparse.ArgumentParser(description="Script for inference pipeline.")
	parser.add_argument("--filepath",
											type=str,
											required=True,
											help="Path to PDF file")
											
	parser.add_argument("--context_len",
											type=int,
											required=False,
											default=1,
											help="Length of context in number of sentences")
                      
	parser.add_argument("--k",
											type=int,
											required=False,
											help="Number of results")

	parser.add_argument("--question",
											type=str,
											required=False,
											help="Question to ask")
                    


	args = parser.parse_args()
	return args

if __name__ == '__main__':
  args = passed_arguments()
  length = args.context_len
  filepath = args.filepath
  question = args.question
  k = args.k
  filestring = convert_pdf_to_string(filepath)
  context = convert_string_to_context(filestring, length)
  cosine_similarity(k, question, context)
  

