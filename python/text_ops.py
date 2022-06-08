import string
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import numpy as np


def word_token_drop_sw(raw_text: str, stopwords_set: set):
    """
    Processes scraped text by dropping stop words & indexing text
    input: raw_text: string of text returned from webscraper
    input: stopwords_set: set of English stopwords to be dropped from raw text
    output: out_text
    """
    # Tokenize text into sentences
    sent_tokens = sent_tokenize(raw_text)
    # Tokenize sentences into words & drop punctuation
    word_tokens = []
    for sent in sent_tokens:
        sent = sent.strip(string.punctuation)
        word_tokens.append(word_tokenize(sent))
    # Filter out drop words
    filtered_sentence = []
    for w in word_tokens:
        if w not in stopwords_set:
            filtered_sentence.append(w)

    return filtered_sentence