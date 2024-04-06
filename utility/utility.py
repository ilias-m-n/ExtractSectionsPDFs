import fitz
import os
import re
from collections import Counter

import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import string
import spacy



def load_file_fitz(path):
    return fitz.open(path)

# Clean Text Preliminary
def full_process_text(text):
    text = text.lower()

    punctuation_except_dots = string.punctuation.replace('.', '') + "’‘"
    text = text.translate(str.maketrans('', '', punctuation_except_dots))

    # tokenization
    tokens = nltk.word_tokenize(text)

    # stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens if token != '.']

    # lemmatization
    lemmatizer = WordNetLemmatizer()
    lemma_tokens = [lemmatizer.lemmatize(token) for token in stemmed_tokens]

    text = " ".join(lemma_tokens)
    return text
