

from datasets import load_dataset
import nltk
nltk.download('punkt')
import numpy as np
import random
import string
from models import InferSent
import torch

'''
Sentences is the list of answers
Question is the list of questions
'''
def inferSent(sentences, question):

    V = 2
    MODEL_PATH = 'encoder/infersent%s.pkl' % V
    params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                    'pool_type': 'max', 'dpout_model': 0.0, 'version': V}

    #begin model training
    infersent = InferSent(params_model)
    infersent.load_state_dict(torch.load(MODEL_PATH))
    W2V_PATH = 'fastText/crawl-300d-2M.vec'
    infersent.set_w2v_path(W2V_PATH)
    infersent.build_vocab(sentences, tokenize=True)
    embeddings = infersent.encode(sentences, tokenize=True)
    q_emb = infersent.encode(question, tokenize = True)

    return embeddings, q_emb

'''
Function to generate cossin similarity score matrix
'''
def cossin_sim_scores(sentences, question):
    sent_norm = sentences / sentences.sum(axis=1)[:,np.newaxis]
    ques_norm = question / question.sum(axis=1)[:,np.newaxis]
    dot = np.dot(ques_norm, sent_norm.T)
    print(dot.shape)
    return dot


'''
Returns the accuracy of the model, each prediction is assigned 1 if the correct answer lies in the top n 
answers and 0 if not
'''
def get_top_n(dotprods, n=5):
    #sort the 
    print('Checking top ', n, ' articles')
    hit = 0
    index = 0
    top_n = dotprods.argsort(axis=1)[:,-n:]
    sort = dotprods.argsort(axis=1)
    for i in range (len(dotprods)):
        if i in top_n[i]:
            hit +=1
        index += np.where(sort[i] == i)[0]
    acc, avg = hit/len(dotprods), index/len(dotprods)
    print(acc, avg)
    return acc, avg

def first(example):
    e = ''
    e = str(example['text'][0])
    return e


'''
Function that gets the list of question and answers from dataset
'''
def dataset():
    ds = load_dataset("eli5", split='train_eli5')
    questions = ds['title']
    a = ds['answers']
    answers = (list(map(first, a)))
    print('number of samples: ', len(answers))
    return questions, answers


def evaluate():
    #get the question and answers from the eli5 training set
    questions, answers = dataset()
    #get the inferSent embeddings of the questions and answers
    embs, q_embs = inferSent(answers[:2000], questions[:2000])
    #compute the cossin similarity socres
    scores = cossin_sim_scores(embs, q_embs)
    #get top n accuracy
    acc1 , avg1 = get_top_n(scores, n=10)
    acc2 , avg2 = get_top_n(scores, n=100)
    acc3 , avg3 = get_top_n(scores, n=1000)
    



if __name__ == '__main__':
    evaluate()  
    
