"""Utility module for MyCourseIndex containing all standard functions.

This module loads all of the needed preprocessing steps / functions that are
used in all other modules.
"""

from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
import spacy
# from piazza_api import Piazza

# EMPLOY CONSTANTS USED THROUGHOUT THE FILE AND CAN BE IMPORTED
sp = spacy.load('en_core_web_sm') #TODO This is for speed
ps = PorterStemmer()


def tokenize_NLTK(text):
    """Tokenize and Stem text using NLTK package and built in functions.

    Note that this function does not actively remove or account for stop
    words or any other method of filtering out words / punctuation.
    
    :param text: The text to tokenize and stem in American English
    :type text: str
    :return: List of tokenized word stems 
    :rtype: List[str]
    """
    text = text.lower()
    tokenized = word_tokenize(text)
    return [ps.stem(w) for w in tokenized]


def tokenize_SpaCy(text):
    """Tokenize and Lemmatize text using SpaCy package.
    
    Note that this fucntion does actively remove all punctuation and accounts
    for whether words are stop words.
    
    :param text: The text to tokenize and stem in American English
    :type text: str
    :return: List of tokenized word stems 
    :rtype: List[str]
    """
    text = text.lower()
    tokenized = sp(text)    
    return [w.lemma_ for w in tokenized if not w.is_punct and not w.is_stop and not w.is_space]


def tokenized_already(input):
    #return input[2:]
    return input
