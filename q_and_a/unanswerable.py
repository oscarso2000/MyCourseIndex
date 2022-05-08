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
    BertModel,
    #AutoTokenizer,
    #AutoModelForQuestionAnswering
)

import argparse
from collections import Counter

from sklearn.linear_model import LogisticRegression
import requests


def passed_arguments():
    parser = argparse.ArgumentParser(description="Script to evaluate model predictions.")
    #parser.add_argument("--model",
    #                    type=int,
    #                    required=True,
    #                    help="Baseline model to test on. \n0 = BERT\n1=DistilBERT")

    parser.add_argument("--data_path",
                        type=str,
                        required=True,
                        help="Path to evaluation dataset")

    #parser.add_argument("--impossible_on",
    #                    type=int,
    #                    required=True,
    #                    help="0: no impossible questions\n1: impossible questions")

    args = parser.parse_args()
    return args


#helper returning the most frequent of a an array:
def most_frequent(List): 
    counter = 0
    num = List[0]  
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 
    return num

# 1 when is_impossible, else 0
def process_json(data_path):
    print("starting yay")
    question = []
    text = []
    answer = []
    is_impossible = []
    ids = []
    num_questions = [] # number of questions asked on the same context

    r = requests.get(url = data_path)
    data = r.json()["data"]
    data_len = len(data)
    for d in data:
        for p in d["paragraphs"]:
            context = p["context"]
            context_len = len(context)
            num = 0
            for qa in p["qas"]:
                quest = qa["question"]
                quest_len = len(quest)
                if (context_len+quest_len < 509):
                    question.append(quest)
                    if (len(qa["answers"])) != 0:
                        an = []
                        for i in qa["answers"]:
                            an.append(i["text"])
                        answer.append(most_frequent(an))
                            
                    else:
                        answer.append("<No Answers>")
                    if qa["is_impossible"]:
                        is_impossible.append(1)
                    else:
                        is_impossible.append(0)
                    ids.append(qa["id"])
                    num += 1
            if (num != 0):
                text.append(context)
                num_questions.append(num)
    print("done")
    return question, text, answer, is_impossible, ids, num_questions


def process_data(question, text, num_questions):
    print("oho")
    input_text = []
    for i in range(len(num_questions)):
        for j in range(num_questions[i]):
            input_text.append( "[CLS] " + question[j] + " [SEP] " + text[i] + " [SEP]")
    return input_text

#return the max_len, is_impossible, and CLS token of SQUAD dataset. Store the data in CSV file
def get_CLS(percentage):
    question, text, answer, is_impossible, ids, num_questions = process_json("https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json")
    input_text = process_data(question, text, num_questions)
    print("done")
    input_text = input_text[int(percentage*len(input_text)):]
    is_impossible = is_impossible[int(percentage*len(is_impossible)):]   
    
    print(len(input_text))
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    print("working")
    input_ids = []
    max_len = 0
    for text in input_text:
        input_id = tokenizer.encode(text)
        input_ids.append(input_id)
        if len(input_id) > max_len:
            max_len = len(input_id)
    
    #append the maximum length of the sentence to the list of is_impossible
    is_impossible.append(max_len)
    is_impossible.to_csv("is_impossible.csv", encoding='utf-8', index=False)
    
    padded = np.array([i + [0]*(max_len - len(i)) for i in input_ids])
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded)
    print(input_ids.size)
    attention_mask = torch.tensor(attention_mask)
    print(attention_mask.size)
    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask = attention_mask)
        print(last_hidden_states)
        features = pd.DataFrame(last_hidden_states[0][:,0,:].numpy())
        print(features)
        features.to_csv("features.csv", encoding='utf-8', index=False)
        
    return features, is_impossible, max_len


#pretrained logistic regression
def logisticReg():
    question, text, answer, is_impossible, ids, num_questions = process_json("https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json")
    input_text = process_data(question, text, num_questions)
    print("done")
    input_text = input_text[int(.99*len(input_text)):]
    is_impossible = is_impossible[int(.99*len(is_impossible)):]
    is_impossible.to_csv("is_impossible.csv", encoding='utf-8', index=False)
    print(len(input_text))
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    print("working")
    input_ids = []
    max_len = 0
    for text in input_text:
        input_id = tokenizer.encode(text)
        input_ids.append(input_id)
        if len(input_id) > max_len:
            max_len = len(input_id)
    padded = np.array([i + [0]*(max_len - len(i)) for i in input_ids])
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded)
    print(input_ids.size)
    attention_mask = torch.tensor(attention_mask)
    print(attention_mask.size)
    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask = attention_mask)
        print(last_hidden_states)
        features = last_hidden_states[0][:,0,:].numpy()
        print(features)
    features.to_csv("features.csv", encoding='utf-8', index=False)
    log_model = LogisticRegression()
    log_model.fit(features,is_impossible)
    print("finished")
    return log_model, max_len


    
#pre-trained bert runs on evaluation sets
#return list of tokens for each question id
def predictions(input_text, print_some_outputs = True):
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    tokenizer_bert = BertTokenizer.from_pretrained('bert-base-uncased')
    model_bert = BertModel.from_pretrained('bert-base-uncased')
    input_ids = []
    token_type_ids = []
    preds = []
    f = []
    print("training")
    log_model, max_len= logisticReg()
    print("lets train")
    for text in input_text:
        input_log = tokenizer_bert.encode(text)
        input_log = input_log + [0] * (max_len - len(input_log))
        attention_mask = [0 if i == 0 else 1
                  for i in input_log]
        input_logs = torch.tensor([input_log])
        print(input_logs.size)
        attention_mask = torch.tensor([attention_mask])
        print(attention_mask.size)
        with torch.no_grad():
            last_hidden_states = model_bert(input_logs,attention_mask = attention_mask)
            print(last_hidden_states)
            features = last_hidden_states[0][:,0,:].numpy()
            print(features)
        f.append(features)
        pred = log_model.predict(features)
        if pred > 0:
            preds.append("<No Answer>")
        else:
            input_ids = tokenizer.encode(text)
            token_type_ids = [0 if i <= input_ids.index(102) else 1
                  for i in range(len(input_ids))]
            start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
            all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
            preds.append((all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1]))
        f.to_csv("features_pred.csv", encoding='utf-8', index=False)
    return preds


#returns the precision, recall, and f1 score
#preds and labels should be tokenized
def evaluate(preds, labels, questions, ids):
    print(len(preds))
    print(len(labels))
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

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



def main(data_path):
    print('Starting baseline evaluation\n')

    question, text, labels, is_impossible, ids, num_questions = process_json(data_path)

    print(len(question))
    print(len(labels))

    input_text = process_data(question, text, num_questions)
    print(len(input_text))
    

    print("Starting predictions")
    preds = predictions(input_text)

    print("Evaluating predictions")
    p, r, f1 = evaluate(preds, labels, question, ids)

    #print some stats
    print('\nEvaluation Stats are: ')
    print('\tPrecision: ', p)
    print('\tRecall: ', r)
    print('\tF1 score: ', f1)

if __name__ == '__main__':
    args = passed_arguments()
    #model_id = args.model
    data_path = args.data_path
    #imp_toggle = args.impossible_on
    main(data_path)