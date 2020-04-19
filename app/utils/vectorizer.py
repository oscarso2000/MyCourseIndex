from sklearn.feature_extraction.text import TfidfVectorizer
from app.utils import tokenize

tokenizer = tokenize.tokenized_already

# S3 JSON Format:
# { "CS4300": {"Piazza": {PostID: content, PostID2: content2}, "Textbook": {DocId: content, DocID2: content2} } }

fromS3 = loadJSONFILE from S3 !!!

docVecDictionary = {}
courseDocDictionary = {}

for course in fromS3:
    vec = TfidfVectorizer(tokenizer = tokenizer)
    documents = []
    for source in course.value:
        for content in source.value:
            unique = [source.key, content.key]
            unique.extend(content.value)
            #looks like ["Piazza", "671", "this", "is", "the", "post"]      
            documents.append(unique)
    docVecDictionary[course.key] = vec.fit_transform(documents).toarray()
    courseDocDictionary[course.key] = documents #[["Piazza", "671", "this", "is", "the", "post"],["Piazza", "672", "this", "is", "the", "post"]]
    
#docVecDictionary is full dictionary of all documents in all courses. Should be a global variable.
