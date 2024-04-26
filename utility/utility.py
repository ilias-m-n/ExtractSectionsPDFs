import string

import fitz
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from tiktoken import get_encoding
import cv2
import numpy as np
from PIL import Image
from transformers import pipeline
from spellchecker import SpellChecker


def load_file_fitz(path):
    return fitz.open(path)

def remove_extra_spaces(text):
    return " ".join(text.split())

def correct_text(text):
    spell = SpellChecker()

    # Find those words in the text that may be misspelled
    misspelled = spell.unknown(text.split())

    corrected_text = []
    for word in text.split():
        # If the word is misspelled, suggest the most likely correction
        if word in misspelled:
            corrected_word = spell.correction(word)
            if not corrected_word:
                continue
            corrected_text.append(corrected_word)
        else:
            corrected_text.append(word)

    # Join corrected words back into a string
    return ' '.join(corrected_text)

def preprocess_image_for_ocr(img):

    img = np.array(img)

    # If the image is in RGB (3 channels), convert it to BGR for OpenCV
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to binarize the image
    # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    _, binary = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)

    # back to pillow format
    img_pil = Image.fromarray(binary)

    img_pil.show()

    return img_pil

# Clean Text Preliminary
def full_process_text(text):
    text = text.lower()

    punctuation_except_dots = string.punctuation.replace('.', '') + '’‘“”„'
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

def full_process_text_keep_sentence_dots(text):
    text = text.lower()

    punctuation_except_dots = string.punctuation.replace('.', '') + '’‘“”„'
    text = text.translate(str.maketrans('', '', punctuation_except_dots))

    # tokenization
    tokens = nltk.word_tokenize(text)

    # stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) if token != '.' else token for token in tokens]

    # lemmatization
    lemmatizer = WordNetLemmatizer()
    lemma_tokens = [lemmatizer.lemmatize(token) if token != '.' else token for token in stemmed_tokens]

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
    punctuation_except_dots = string.punctuation.replace('.', '').replace("'", '') + "’‘“”„"
    text = text.translate(str.maketrans('', '', punctuation_except_dots))
    return text

def full_clean_text_keep_sent_struc(text):
    punctuation_except_dots = string.punctuation.replace('.', '') + '’‘“”„'
    text = text.translate(str.maketrans('', '', punctuation_except_dots))

    # tokenization
    tokens = nltk.word_tokenize(text)

    sentences = []

    curr = []
    for token in tokens:
        curr.append(token)
        if token == '.':
            sentences.append(' '.join(curr))
            curr = []
    if len(curr) != 0:
        sentences.append(' '.join(curr))

    return sentences





# Estimate number of tokens
def count_tokens(text: str, encoding: str = "cl100k_base") -> int:
    encoding = get_encoding(encoding)
    return len(encoding.encode(text))

# prepare anchors for text extraction
def prep_extract_anchors(anchor, wild_c):
    anchor = anchor.replace(' ... ', r'(?:(?!\s\.\s).){,' + wild_c + '}?')
    anchor = anchor.replace(' --- ', r'(?!\sconsolidated\s\b)\b\w*')
    anchor = anchor.replace(' .... ', r'\s(our|my)\s')
    return anchor


def merge_overlapping_intervals(intervals):
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = []

    for interval in sorted_intervals:
        # If the list of merged intervals is empty or if the current
        # interval does not overlap with the previous, simply append it.
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            # Otherwise, there is an overlap, so merge the current and previous intervals
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))

    return merged

def get_num_workers(prompt, lower_bound, upper_bound):
    while True:
        try:
            user_input = input(prompt)
            number = int(user_input)
            if lower_bound <= number <= upper_bound:
                return number
            else:
                print(f"Please enter a number within the bounds ({lower_bound}, {upper_bound}).")
        except ValueError:
            print("The input is not a valid integer. Please try again.")