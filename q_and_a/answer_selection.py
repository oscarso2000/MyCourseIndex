#import
import torch
from torch.nn.functional import softmax
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from tqdm import tqdm, trange
import io
import json
import os
import numpy as np
from transformers import (
    BertTokenizer,
    BertForQuestionAnswering,
)
import argparse
import requests


#argments
def passed_arguments():
	parser = argparse.ArgumentParser(description="Script to evaluate model predictions.")

	parser.add_argument("--data_path",
											type=str,
											required=True,
											help="Path to evaluation dataset")
	args = parser.parse_args()
	return args

    parser.add_argument("--top_n",
											type=int,
											required=False,
                                            default=1,
											help="Top n results to consider correct")
	args = parser.parse_args()
	return args

    parser.add_argument("--propose_cnt",
											type=int,
											required=False,
                                            default=10,
											help="Number of contexts to test question on")
	args = parser.parse_args()
	return args


def wrap_select(a, i, n):
    """
    a - list to select from
    i - index of a to start from
    n - number of things to select
    """
    b = []

    #true answer as first possition
    b.append(a[i])
    j = (i+1)%len(a)
    while len(b) < n+1 :
        if a[j] not in b:
            b.append(a[(j)])
        j = (j+1)%len(a)
    return b


def process_data_mult_text(question, contexts):
    """
    Adds CLS, and SEP tokens to input text
    Run through tokenizer 
    Returns tokenized
    """ 
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

    input_text = []
    input_ids = []
    token_type_ids = []
    for i in range(len(contexts)):
        text =  "[CLS] " + question + " [SEP] " + contexts[i] + " [SEP]"
        input_text.append(text)

        encoded = tokenizer.encode(text)
        input_ids.append(encoded)

        token_type_id = [0 if i <= encoded.index(102) else 1 ]
        token_type_ids.append(token_type_id)

    return input_text, input_ids, token_type_ids


def get_3110_set(data_path, include_impossible = False):
    """Returns the 3110 dataset data.
    """
    cwd = os.getcwd()

    question, text, answer, labels, ids, is_impossible = [], [], [], [], [], []
    with open(data_path) as f:
        data = json.load(f)["data"]
    
    for d in data:
        if (include_impossible or d["is_impossible"]==0 ):
            is_impossible.append(1 if d["is_impossible"] else 0)
            question.append(d["question"])
            text.append(d["context"])
            answer.append(d["answer"])
            ids.append(d["id"])

    return question, text, answer, is_impossible



def evaluate_on_multiple_context(questions, contexts, answers, eval_on = 10, top_n = 1):

    
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    results = np.zeros(len(questions))

    for i,q in enumerate(questions):

        #get possible passages to test question on
        context_sub = wrap_select(contexts, i, eval_on)

        #format questions and context for bert input
        input_text, input_ids, token_type_ids = process_data_mult_text(q, context_sub)
        scores_avg = np.zeros(eval_on)

        #pass input through bert saving avg of max value in logits
        for j in range (eval_on):
            start_scores, end_scores = model(torch.tensor([input_ids[j]]), token_type_ids=torch.tensor([token_type_ids[j]]), return_dict=False)   
            soft_start = softmax(start_scores)
            soft_end = softmax(end_scores)
            scores_avg[j] = (torch.max(soft_start) + torch.max(soft_end))/2         

        arr = scores_avg.argsort()[-top_n:][::-1]
        results[i] = 1 if 0 in arr else 0


    return results


def main(data_path, top_n, propose_cnt):

    print('Getting data')
    questions, contexts, answers, is_impossible = get_3110_set(data_path)

    print("Beginning Evaluation")
    results = evaluate_on_multiple_context(questions, contexts, answers, eval_on=p_cnt, top_n=top_n)
    print("Finished Evaluation")
    print("Acc: ", np.sum(results)/len(results))


if __name__ == '__main__':
    args = passed_arguments()
    data_path = args.data_path
    top_n = args.top_n
    p_cnt = arg.propose_cnt

    main(data_path, top_n, p_cnt)