from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import numpy.linalg as LA
import app.utils as utils
import time

def cosineSim(query, courseVecDictionary, course, logger):
    #courseVecDictionary[class selected]
    vec, docVectorizerArray = courseVecDictionary[course]
    
    query = utils.tokenize_SpaCy(query)
    queryVectorizerArray = np.zeros((docVectorizerArray.shape[1],))
    feature_list = vec.get_feature_names()

    for w in query:
        idx = feature_list.index(w)
        queryVectorizerArray[idx] += 1.0

    # queryVectorizerArray = vec.transform(query).toarray()[0]
    
    # print('Fit Vectorizer to train set', docVectorizerArray.shape)
    # print('Transform Vectorizer to test set', queryVectorizerArray.shape)

    num = queryVectorizerArray.dot(docVectorizerArray.T)
    denom = LA.norm(queryVectorizerArray)*LA.norm(docVectorizerArray,axis=1)
    sim = num/denom

    return sim




#for local use
if __name__ == "__main__":
    
    #instead, require sheetal's preprocessed "content"
    from nltk.tokenize import sent_tokenize
    documents = sent_tokenize("".join(open('alice29.txt').readlines()))
     
    
    #documents = ["The sky is blue.", "The sun is bright."] 
    query = ["Alice loves the sun."]
    
    #stopWords = stopwords.words('english')
    #stopWords = utils.sp.Defaults.stop_words
    
    tokenizer = utils.tokenize_SpaCy
    
    #vectorizer = TfidfVectorizer(stop_words = stopWords, tokenizer = tokenizer)
    vectorizer = TfidfVectorizer(tokenizer = tokenizer)
    
    #Dictionary that maps class instance to the tfidf vectorizer for the particular class. 
    courseVecDictionary = {"CS 4300": vectorizer.fit_transform(documents).toarray()}
    
    # print(cosineSim(query, courseVecDictionary, vectorizer))
    returnedResults = cosineSim(query, courseVecDictionary, "CS 4300")
    print([documents[x] for x in returnedResults])