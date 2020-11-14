import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from tqdm import tqdm, trange
import pandas as pd
import io
import json
import os
import numpy as np
import random
from transformers import (
    BertTokenizer,
    BertForQuestionAnswering,
    AutoTokenizer,
    AutoModelForQuestionAnswering
)

import argparse
from collections import Counter


def passed_arguments():
	parser = argparse.ArgumentParser(description="Script to evaluate model predictions.")
	parser.add_argument("--model",
											type=int,
											required=True,
											help="Baseline model to test on. \n0 = BERT\n1=DistilBERT")

	parser.add_argument("--data_path",
											type=str,
											required=True,
											help="Path to evaluation dataset")

	parser.add_argument("--impossible_on",
											type=int,
											required=True,
											help="0: no impossible questions\n1: impossible questions")

	args = parser.parse_args()
	return args


# imp_toggle = true if want to include impossible
def process_json(data_path, imp_toggle):
  question = []
  text = []
  answer = []
  is_impossible = []
  ids = []
  with open(data_path) as f:
    data = json.load(f)["data"]
  
  for d in data:
    if (not d["is_impossible"] or imp_toggle):
      question.append(d["question"])
      text.append(d["context"])
      answer.append(d["answer"])
      is_impossible.append(d["is_impossible"])
      ids.append(d["id"])

  return question, text, answer, is_impossible, ids

def process_data(question, text):
  input_text = []
  for i in range(len(question)):
    input_text.append( "[CLS] " + question[i] + " [SEP] " + text[i] + " [SEP]")

  return input_text


#returns the tokenizer and model associated with the model id
# 0 = bert
# 1 = distilbert
def model_pick(id):
  if (id == 0):
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
  if (id == 1):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
    model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")

  return tokenizer, model


#pre-trained bert runs on evaluation sets
#return list of tokens for each question id
def predictions(model_id, input_text, print_some_outputs = True):

  tokenizer, model = model_pick(model_id)
 
  input_ids = []
  token_type_ids = []
  preds = []
  for text in input_text:

    if model_id == 0:

      input_ids = tokenizer.encode(text)
      token_type_ids = [0 if i <= input_ids.index(102) else 1 
        for i in range(len(input_ids))]
    
      start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))    
      all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
      preds.append((all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1]))

    elif model_id == 1:
      input_ids = tokenizer.encode(text)
      token_type_ids = [0 if i <= input_ids.index(102) else 1 
        for i in range(len(input_ids))]
    
      start_scores, end_scores = model(torch.tensor([input_ids]))    
      all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
      preds.append((all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1]))

  return preds


#returns the precision, recall, and f1 score
#preds and labels should be tokenized
def evaluate(preds, labels, questions, ids, model_id):

  tokenizer, _ = model_pick(model_id)

  labels_tok = []
  for l in labels:
    encoded = tokenizer.encode(l)
    to_tok = tokenizer.convert_ids_to_tokens(encoded)
    labels_tok.append(to_tok[1:-1])

  n = len(labels)
  precision = 0
  recall = 0
  f1 = 0

  for i in range(len(labels_tok)):
   
    p = preds[i]
    l = labels_tok[i]

    if len(p) == 0 or len(l) == 0:
      agree = 1 if len(p) == len(l) else 0
      precision += 1
      recall += 1
      f1 += 1

    else:
      common_toks = Counter(p) & Counter(l)
      intersection = 1.0 * sum(common_toks.values())
      #calculate precision
      pr = intersection/ len(p)
      re = intersection / len(l)
      precision += pr
      #calculate recall
      recall += re
      #calculate f1
      f1 += 0 if (pr == 0 or re == 0) else (2*pr*re)/(pr+re)
      if (pr == 0 or re == 0):

        print("\nBad answer example ",ids[i], ': ', questions[i])
        print("Prediction: ", ' '.join(p))
        print("Answer: ", ' '.join(l))

  #average over all samples
  precision = precision/n
  recall = recall/n
  f1 = f1/n

  return precision, recall, f1



def main(model_id, data_path, imp_toggle):
  print('Starting baseline evaluation\n')

  if model_id == 0:
    print("Picked bert")
  elif model_id ==1:
    print("Picked distilbert")

  question, text, labels, _, ids = process_json(data_path, imp_toggle)

  if imp_toggle:
    print("Testing impossible questions")
  else:
    print("Not testing impossible questions")

  input_text = process_data(question, text)

  print("Starting predictions")
  preds = predictions(model_id, input_text)

  print("Evaluating predictions")
  p, r, f1 = evaluate(preds, labels, question, ids, model_id) 

  #print some stats
  print('\nEvaluation Stats are: ')
  print('\tPrecision: ', p)
  print('\tRecall: ', r)
  print('\tF1 score: ', f1)

if __name__ == '__main__':
  args = passed_arguments()
  model_id = args.model
  data_path = args.data_path
  imp_toggle = args.impossible_on
  main(model_id, data_path, imp_toggle)