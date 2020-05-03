from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import numpy.linalg as LA
import app.utils as utils
import time

def cosineSim(query, courseVecDictionary, course, reverseIndexDictionary):
    #courseVecDictionary[class selected]
    vec, docVectorizerArray = courseVecDictionary[course]
    reverse_index = reverseIndexDictionary[course]
    
    query = utils.tokenize_SpaCy(query)
    queryVectorizerArray = np.zeros((docVectorizerArray.shape[1],))
    # feature_list = vec.get_feature_names()

    for w in query:
        idx = reverse_index.get(w, -1)
        if idx > 0:
            queryVectorizerArray[idx] += 1.0
        # try:
        #     idx = feature_list.index(w)
        #     queryVectorizerArray[idx] += 1.0
        # except ValueError:
        #     pass
    queryVectorizerArray *= vec.idf_
    
    if queryVectorizerArray.sum() == 0:
        return []

    # queryVectorizerArray = vec.transform(query).toarray()[0]
    
    # print('Fit Vectorizer to train set', docVectorizerArray.shape)
    # print('Transform Vectorizer to test set', queryVectorizerArray.shape)

    num = queryVectorizerArray.dot(docVectorizerArray.T)
    denom = LA.norm(queryVectorizerArray)*LA.norm(docVectorizerArray,axis=1)
    sim = num/denom

    return sim

def cosineSimSplit(query, courseVecDictionary, course): #not working
    vec, piazzaDocVectorizerArray, otherDocVectorizerArray = courseVecDictionary[course]
    query = utils.tokenize_SpaCy(query)
    
    queryPiazzaVectorizerArray = np.zeros((piazzaDocVectorizerArray.shape[1],))
    queryOtherVectorizerArray = np.zeros((otherDocVectorizerArray.shape[1],))
    feature_list = vec.get_feature_names()

    for w in query:
        try:
            idx = feature_list.index(w)
            queryPiazzaVectorizerArray[idx] += 1.0
        except ValueError:
            pass
        
    for w in query:
        try:
            idx = feature_list.index(w)
            queryOtherVectorizerArray[idx] += 1.0
        except ValueError:
            pass
    if queryPiazzaVectorizerArray.sum() == 0 and queryOtherVectorizerArray.sum() == 0:
        return [], [], [], []
    elif queryPiazzaVectorizerArray.sum() == 0:
        other_num = queryOtherVectorizerArray.dot(otherDocVectorizerArray.T)
        other_denom = LA.norm(queryOtherVectorizerArray)*LA.norm(otherDocVectorizerArray,axis=1)
        other_sim = other_num/other_denom
        return [], [], other_sim, other_sim > 0  
    elif queryOtherVectorizerArray.sum() == 0:
        piazza_num = queryPiazzaVectorizerArray.dot(piazzaDocVectorizerArray.T)
        piazza_denom = LA.norm(queryPiazzaVectorizerArray)*LA.norm(piazzaDocVectorizerArray,axis=1)
        piazza_sim = piazza_num/piazza_denom
        return piazza_sim, piazza_sim>0, [],[]
        
    piazza_num = queryPiazzaVectorizerArray.dot(piazzaDocVectorizerArray.T)
    piazza_denom = LA.norm(queryPiazzaVectorizerArray)*LA.norm(piazzaDocVectorizerArray,axis=1)
    piazza_sim = piazza_num/piazza_denom
    
    other_num = queryOtherVectorizerArray.dot(otherDocVectorizerArray.T)
    other_denom = LA.norm(queryOtherVectorizerArray)*LA.norm(otherDocVectorizerArray,axis=1)
    other_sim = other_num/other_denom
    
    return piazza_sim, piazza_sim > 0 , other_sim , other_sim > 0
    
def LSI_SVD(query, courseVecDictionary, course, reverseIndexDictionary, svdDictionary):
    #courseVecDictionary[class selected]
    vec, docVectorizerArray = courseVecDictionary[course]
    reverse_index = reverseIndexDictionary[course]

    query = utils.tokenize_SpaCy(query)
    queryVectorizerArray = np.zeros((docVectorizerArray.shape[1],))
    # feature_list = vec.get_feature_names()

    for w in query:
        idx = reverse_index.get(w, -1)
        if idx > 0:
            queryVectorizerArray[idx] += 1.0
    queryVectorizerArray *= vec.idf_
    
    if queryVectorizerArray.sum() == 0:
        return []
        
    k = 500
    # u,s,v_t = np.linalg.svd(docVectorizerArray.T) #svd on tfidf documents
    u,s,v_t = svdDictionary[course]
    q = queryVectorizerArray
    q_hat = np.matmul(np.transpose(u[:,:k]),q)
    
    sim = []
    for i in range(docVectorizerArray.shape[0]):
        num = np.matmul(np.matmul(np.diag(s[:k]),v_t[:k,i]),np.transpose(q_hat))
        denom = np.linalg.norm(np.matmul(np.diag(s[:k]),v_t[:k,i]))*np.linalg.norm(q_hat)
        sim.append(num/denom)

    return np.array(sim)
    
    
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
