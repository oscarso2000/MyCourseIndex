# import these modules 
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
import spacy
sp = spacy.load('en_core_web_lg')

def tokenize_NLTK(text):
    """Returns a list of words that make up the text.
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Params: {text: String}
    Returns: List
    """
    text = text.lower()
    ps = PorterStemmer() 
    tokenized = word_tokenize(text)
    return [ps.stem(w) for w in tokenized]

#we are using this one below.
def tokenize_SpaCy(text):
    """Returns a list of words that make up the text.
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Params: {text: String}
    Returns: List
    """
    text = text.lower()
    tokenized = sp(text)    
    return [w.lemma_ for w in tokenized if not w.is_punct and not w.is_stop]