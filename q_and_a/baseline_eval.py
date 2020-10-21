import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from tqdm import tqdm, trange
import pandas as pd
import io
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


#####Global variables

# need the path to the eval data

def passed_arguments():
	parser = argparse.ArgumentParser(description="Script to evaluate model predictions.")
	parser.add_argument("--model",
											type=int,
											required=True,
											help="Baseline model to test on. \n0 = BERT\n1=DistilBERT")
	args = parser.parse_args()
	return args

#list of question, text
#question, text = "What day is it today?", "My name is Mike and I live in Ithaca."
def process_data(question, text):
  input_text = []
  for i in range(len(question)):
    input_text.append( "[CLS] " + question[i] + " [SEP] " + text[i] + " [SEP]")

  return input_text


#returns the tokenizer and model associated with the model id
# 0 = bert
# 1 = distilbert
def model_pick(id):
  tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
  model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
  if (id == 1):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
    model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")

  return tokenizer, model


#pre-trained bert runs on evaluation sets
#return list of tokens for each question id
def predictions(model_id, input_id, input_text, print_some_outputs = True):

  tokenizer, model = model_pick(model_id)
 
  input_ids = []
  token_type_ids = []
  preds = []
  for text in input_text:

    input_ids = tokenizer.encode(text)
    token_type_ids = [0 if i <= input_ids.index(102) else 1 
      for i in range(len(input_ids))]
  
    start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))    
    all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    preds.append((all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1]))
    #print('result: ', ' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1]))

  return preds


#returns the precision, recall, and f1 score
#preds and labels should be tokenized
def evaluate(preds, labels, model_id):

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
      precision += intersection/ len(p)
      #calculate recall
      recall += intersection / len(l)
      #calculate f1
      f1 += 0 if (precision == 0 or recall == 0) else 2*precision*recall/(precision+recall)

  #average over all samples
  precision = precision/n
  recall = recall/n
  f1 = f1/n

  return precision, recall, f1



def main(model_id):
  print('Starting baseline evaluation\n')
  question = ['Where does Bob live??']
  text = ['Bob lives in Ithaca with his mom.']
  labels = ['Ithaca']
  input_id = 0
  input_text = process_data(question, text)

  preds = predictions(model_id, input_id, input_text)
  p, r, f1 = evaluate(preds, labels, model_id) 
  print('Evaluation Stats are: ')
  print('\tPrecision: ', p)
  print('\tRecall: ', r)
  print('\tF1 score: ', f1)

if __name__ == '__main__':
  args = passed_arguments()
  model_id = args.model
  main(model_id)