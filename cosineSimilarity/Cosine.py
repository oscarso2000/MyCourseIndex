from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import numpy.linalg as LA

cosine_function = lambda a, b : round(np.inner(a, b)/(LA.norm(a)*LA.norm(b)), 3)

documents = ["The sky is blue.", "The sun is bright."]
query = ["The sun in the sky is bright."]
stopWords = stopwords.words('english')

#vectorizer = TfidfVectorizer(stop_words = stopWords)
vectorizer = TfidfVectorizer()

docVectorizerArray = vectorizer.fit_transform(documents).toarray()
queryVectorizerArray = vectorizer.transform(query).toarray()
print('Fit Vectorizer to train set', docVectorizerArray)
print('Transform Vectorizer to test set', queryVectorizerArray)

for vector in docVectorizerArray:
    for queryV in queryVectorizerArray:
        cosine = cosine_function(vector, queryV)
        print(cosine)
