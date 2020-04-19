from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import numpy.linalg as LA
import app.utils as utils
import time

def cosineSim(query, courseVecDictionary, course): #top x highest
    #cosine_function = lambda a, b : round(np.inner(a, b)/(LA.norm(a)*LA.norm(b)), 3)
    #vectorizer = TfidfVectorizer(stop_words = stopWords)
    #start = time.time()
    #docVectorizerArray = vectorizer.fit_transform(documents).toarray()
    #end = time.time()-start

    #courseVecDictionary[class selected]
    docVectorizerArray = courseVecDictionary[course]
    
    query = utils.tokenize_SpaCy(query)
    
    queryVectorizerArray = docVectorizerArray.transform(query).toarray()[0]
    
    print('Fit Vectorizer to train set', docVectorizerArray.shape)
    print('Transform Vectorizer to test set', queryVectorizerArray.shape)

    num = queryVectorizerArray.dot(docVectorizerArray.T)
    denom = LA.norm(queryVectorizerArray)*LA.norm(docVectorizerArray,axis=1)
    sim = num/denom
    
    return sim
    
    # n = 50 #top x highest
    # #returns indices of highest n similarity values
    # reverseList = (-sim).argsort()[:n]
    # print(sim[reverseList])
    
    # return reverseList 
    
    
    
    
    
    # for vector in docVectorizerArray:
    #     for queryV in queryVectorizerArray:
    #         cosine = cosine_function(vector, queryV)
    #         print(cosine)
            
    #print(end)



#for local use
if __name__ == "__main__":
    
    #instead, require sheetal's preprocessed "content"
    from nltk.tokenize import sent_tokenize
    documents = sent_tokenize("".join(open('alice29.txt').readlines()))
     
    
    #documents = ["The sky is blue.", "The sun is bright."] 
    query = ["Alice loves the sun."]
    
    #stopWords = stopwords.words('english')
    #stopWords = utils.sp.Defaults.stop_words
    
    tokenizer = utils.tokenized_SpaCy
    
    #vectorizer = TfidfVectorizer(stop_words = stopWords, tokenizer = tokenizer)
    vectorizer = TfidfVectorizer(tokenizer = tokenizer)
    
    #Dictionary that maps class instance to the tfidf vectorizer for the particular class. 
    courseVecDictionary = {"CS 4300": vectorizer.fit_transform(documents).toarray()}
    
    # print(cosineSim(query, courseVecDictionary, vectorizer))
    returnedResults = cosineSim(query, courseVecDictionary, "CS 4300")
    print([documents[x] for x in returnedResults])