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
    BertConfig,
    AutoTokenizer,
    AutoModelForQuestionAnswering
)
import argparse
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn import metrics
import requests


###GLOBAL VARIABLES
SQUAD2_TRAIN_URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json"
CLS_EMBS_DATASET_INPUT = "cls_emb_input.npy"
EMBS_DATASET_LABELS = "squad_emb_labels.npy"
AVG_EMBS_DATASET_INPUT = "avg_emb_input.npy"
TEST_EMB_DATASET_INPUT = "3110_emb_input.npy"
TEST_EMB_DATASET_LABELS = "3110_emb_labels.npy"

def passed_arguments():
    parser = argparse.ArgumentParser(description="Script to evaluate model predictions.")
    parser.add_argument("--data_path",
                        type=str,
                        required=True,
                        help="Path to evaluation dataset")
    parser.add_argument("--emb_type",
                        type=int,
                        required=False,
                        default=0,
                        help="0 if using cls embedding \n1 if using avg of token embeddings")

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


####################################################################################################
###################      Functions For Processing Data and Generating Datasets    ##################

def process_json(data_path):
    """
    Function that processes squad data 
    Arguments: 
        data_path: the url of the data
    Returns:
        question: list of questions
        text: list of contexts
        answer: list of answers
        is_impossible: if the question is impossible to answer
        ids: the id of each entry
        num_questions: how many questions each context has
    """
    question, text, answer, is_impossible, ids, num_questions = [], [], [], [], [], []
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
    return question, text, answer, is_impossible, ids, num_questions


def process_data(question, text, num_questions):
    """
    Adds CLS, and SEP tokens to input text
    """
    input_text = []
    for i in range(len(num_questions)):
        for j in range(num_questions[i]):
            input_text.append( "[CLS] " + question[j] + " [SEP] " + text[i] + " [SEP]")
    return input_text


def get_cls_from_input(input_text,  is_impossible, emb_type = 0):
    """
    Function that returns CLS embeddings for each entry in input_text
    """
    #BERT model and tokenizer     
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    input_ids = [] #holds all the token id encodings for each input
    features = np.zeros((len(input_text), 768))
    max_len = 0
    for text in input_text:
        input_id = tokenizer.encode(text)
        input_ids.append(input_id)
        if len(input_id) > max_len:
            max_len = len(input_id)

    is_impossible.append(max_len)
    is_impossible = np.array(is_impossible)

    with torch.no_grad():
        for i in range(len(input_ids)):
            input = input_ids[i]
            padded = np.array(input + [0]*(max_len - len(input)))
            attention_mask = np.where(padded != 0, 1, 0)
            input = torch.tensor([padded]).type(torch.LongTensor)
            attention_mask = torch.tensor([attention_mask])
            last_hidden_states = model(input, attention_mask = attention_mask)

            if (emb_type == 0): #cls token
                features[i] = (last_hidden_states[0][:,0,:].numpy())

            elif(emb_type == 1): #avg of work tokens
                token_vecs = last_hidden_states[0][0]
                features[i] = torch.mean(token_vecs, dim=0)


    return features, is_impossible
    

def get_training_set(data_url = SQUAD2_TRAIN_URL, emb_type = 0):
    """
    Returns the CLS tokens from passing the SQUAD 2.0 training set into BERT and labels
    emb_type: 0 if using cls token emb 
              1 if using avg token emb
    """
    cwd = os.getcwd()
    csv_name_input = os.path.join(cwd, CLS_EMBS_DATASET_INPUT ) if emb_type == 0 else os.path.join(cwd, AVG_EMBS_DATASET_INPUT)
    csv_name_labels = os.path.join(cwd, EMBS_DATASET_LABELS )

    #processing squad 2.0 data
    question, text, answer, is_impossible, ids, num_questions = process_json(data_url)
    #format the test to be input into BERT
    input_text = process_data(question, text, num_questions)

    #check if the files exist locally
    if os.path.exists(csv_name_input) and os.path.exists(csv_name_labels):
        print("Found Training Set Locally")
        labels = np.load(csv_name_labels)
        inputs = np.load(csv_name_input)
        max_len = labels[-1]
        labels = labels[:-1]
        return inputs, labels, input_text, max_len

    else:
        features, is_impossible = get_cls_from_input(input_text, is_impossible, emb_type)
        
        np.save(csv_name_input, features)
        np.save(csv_name_labels, is_impossible)
        print(features.shape, is_impossible.shape)
        max_len = is_impossible[-1]
        is_impossible = is_impossible[:-1]

        return features, is_impossible, input_text, max_len


def get_testing_set(data_path, emb_type=0):
    """Returns the CLS tokens embeddings from passing the CS3110 data set into BERT and labels.
    """
    cwd = os.getcwd()
    csv_name_input = os.path.join(cwd,TEST_EMB_DATASET_INPUT )
    csv_name_labels = os.path.join(cwd,TEST_EMB_DATASET_LABELS )

    #process text
    question, text, answer, test_labels, ids, is_impossible, num_questions = [], [], [], [], [], [], []
    with open(data_path) as f:
        data = json.load(f)["data"]
    
    for d in data:
        question.append(d["question"])
        text.append(d["context"])
        answer.append(d["answer"])
        #is_impossible label is 1 if it's not answerable and 0 if it is answerable
        is_impossible.append(1 if d["is_impossible"] else 0)
        ids.append(d["id"])
        num_questions.append(1)

    #format the text to be passed into BERT
        input_text = process_data(question, text, num_questions)

    if os.path.exists(csv_name_input) and os.path.exists(csv_name_labels):
        print("Found Testing Set Locally")
        labels = np.load(csv_name_labels)
        inputs = np.load(csv_name_input)
        max_len = labels[-1]
        labels = labels[:-1]
        return inputs, labels, input_text, max_len
        
    else:
        inputs, labels = get_cls_from_input(input_text, is_impossible, emb_type)
        np.save(csv_name_input, inputs)
        np.save(csv_name_labels, labels)
        max_len = labels[-1]
        labels = labels[:-1]
        return inputs, labels, input_text, max_len

####################################################################################################
###################           Functions For Answerability Classification          ##################

def logisticReg(inputs, labels, test_input, test_labels):
    """Returns the best performing logistic regression model. 
    Function that trains a logistic regression classification model on given training data 
    and then evaluated it on given test data. 
    """
    #establishing ranges for parameters
    perf = 0
    best_c = .001
    best_log = LogisticRegression(C=1)
    c_param_range = [0.001,0.01,0.1,1,10,100]
    for i in c_param_range:
        log_model = LogisticRegression(C=i)
        log_model.fit(inputs,labels)
        #evaluate
        y = log_model.predict(inputs)
        #implement confusion matrix + other metrics
        score = log_model.score(inputs, labels)
        if (perf < score):
            best_c = i
            perf = score 
            best_log = log_model
    print("Best C: ", best_c, " Score: ", perf)   
    train_preds = best_log.predict(inputs)
    cm_train = metrics.confusion_matrix(labels, train_preds)
    print("Confusion matrix training \n", cm_train)
    

    #test on 3110 data
    print("Testing on 3110 Dataset")
    test_preds = best_log.predict(test_input)
    cm = metrics.confusion_matrix(test_labels, test_preds)
    print("Confusion Matrix Testing\n", cm)
    print("Accuracy", best_log.score(test_input, test_labels))
    return best_log


def predictions(input_text, print_some_outputs = True):
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    input_ids = []
    token_type_ids = []
    preds = []
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


def main(data_path, eb=0):

    print('Creating Testing Dataset')
    testing_x, testing_y, input_3110, max_len_test = get_testing_set(data_path, emb_type = eb)
    print("Creating Training Dataset")
    training_x, training_y, input_squad, max_len_train = get_training_set(emb_type = eb)
    

    imp_percent_test = np.sum(testing_y)/len(testing_y)
    imp_percent_train = np.sum(training_y)/len(training_y)
    print("% Impossible in train vs test: ", imp_percent_train, imp_percent_test )

    print("\nUsing Logistic Regression")
    lr_cls = logisticReg(training_x, training_y, testing_x, testing_y)

    
    print("\nStarting predictions")
    #preds = predictions(input_text)

    print("\nEvaluating predictions")
    #   p, r, f1 = evaluate(preds, answers, question, ids)

    #print some stats
    print('\nEvaluation Stats are: ')
    print('\tPrecision: ', p)
    print('\tRecall: ', r)
    print('\tF1 score: ', f1)

if __name__ == '__main__':
    args = passed_arguments()
    data_path = args.data_path
    emb_type = args.emb_type
    main(data_path, emb_type)
