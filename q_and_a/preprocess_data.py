import torch
import pandas as pd
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
)

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
    
def logisticReg():
    #features,is_impossible, max_len = get_CLS()
    is_impossible = pd.read_csv('is_impossible.csv')
    max_len = is_impossible[-1]
    is_impossible = is_impossible[:-1]
    features = pd.read_csv('features.csv')
    
    log_model = LogisticRegression()
    log_model.fit(features,is_impossible)
    print("finished")
    return log_model, max_len

if __name__ == '__main__':    
    get_CLS()