import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler, Dataset,SubsetRandomSampler
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
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torchtext import data
import pandas as pd
import re
import argparse
from collections import Counter
from sklearn.linear_model import LogisticRegression
import requests

class BertBinaryClassifier(nn.Module):
    def __init__(self, dropout=0.1):
        super(BertBinaryClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.linear = nn.Linear(768, 1)
        self.sigmoid = nn.Sigmoid()
        
    
    def forward(self, tokens, mask):
        _, pooled_output = self.bert(tokens)
        linear_output = self.linear(pooled_output)
        proba = self.sigmoid(linear_output)
        return proba

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


def FC(percentage, EPOCHS, BATCH_SIZE):
    question, text, answer, is_impossible, ids, num_questions = process_json("https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json")
    input_text = process_data(question, text, num_questions)
    print("done")
    input_text = input_text[int(percentage*len(input_text)):]
    is_impossible = is_impossible[int(percentage*len(is_impossible)):]   
    
    print(len(input_text))
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_clf = BertBinaryClassifier()
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

    train_tokens_tensor = input_ids[:int(0.8*len(input_ids))]
    train_y_tensor = torch.tensor(is_impossible[:int(0.8*len(input_ids))]).float().reshape(-1,1)
    test_tokens_tensor = input_ids[int(0.8*len(input_ids)):]
    test_y_tensor = torch.tensor(is_impossible[int(0.8*len(input_ids)):]).float().reshape(-1,1)

    train_dataset = TensorDataset(train_tokens_tensor, train_y_tensor)
    train_sampler = RandomSampler(train_dataset)
    train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=BATCH_SIZE)
    test_dataset = TensorDataset(test_tokens_tensor, test_y_tensor)
    test_sampler = SequentialSampler(test_dataset)
    test_dataloader = DataLoader(test_dataset, sampler=test_sampler, batch_size=BATCH_SIZE)

    optimizer = optim.Adam(bert_clf.parameters(), lr=3e-6)
    loss_fn = nn.BCELoss()
    
    bert_clf.train()
    print('Training model...')
    for epoch_num in range(EPOCHS):
        for step_num, (token_ids, labels) in enumerate(train_dataloader):
            probas = bert_clf(token_ids)
            batch_loss = loss_fn(probas, labels)
            bert_clf.zero_grad()
            batch_loss.backward()
            optimizer.step()
            print("epoch_num = " + epoch_num + " step_num = " + step_num)
    print('Training Completed')
    torch.save(bert_clf.state_dict(), "model.pt")

    bert_clf.eval()
    print('Evaluating model...')
    correct = 0
    for batch_index, (input_t, y) in enumerate(test_dataloader):
        preds = bert_clf(input_t)
        p = preds.reshape(-1).detach().numpy().round()
        y1 = y.reshape(-1).detach().numpy()
        for i in range(len(p)):
            if p[i] == y1[i]:
                correct = correct + 1                        
        loss = loss_fn(preds, y)
        print(f"Loss: {loss.detach()}")

    print("Accuracy={}".format(correct/(0.2*len(input_ids))))


if __name__ == '__main__':
    FC(0.95, 5, 32)