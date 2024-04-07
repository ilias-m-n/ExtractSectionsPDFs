import string

import fitz
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from tiktoken import get_encoding


def load_file_fitz(path):
    return fitz.open(path)

def remove_extra_spaces(text):
    return " ".join(text.split())

# Clean Text Preliminary
def full_process_text(text):
    text = text.lower()

    punctuation_except_dots = string.punctuation.replace('.', '') + '’‘“”'
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

# Prep Anchors
def process_section_anchors(section_anchors):
    processed_section_anchors = {}
    for section, parts in section_anchors.items():
        processed_section_anchors[section] = list()
        for part in section_anchors[section]:
            processed_part = tuple([full_process_text(p) for p in part])
            processed_section_anchors[section].append(processed_part)
    return processed_section_anchors

def full_clean_text(text):
    punctuation_except_dots = string.punctuation.replace('.', '').replace("'", '') + "’‘“”"
    text = text.translate(str.maketrans('', '', punctuation_except_dots))
    return text


# Estimate number of tokens
def count_tokens(text: str, encoding: str = "cl100k_base") -> int:
    encoding = get_encoding(encoding)
    return len(encoding.encode(text))