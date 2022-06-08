import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import numpy as np


def text_preprocessing(raw_text: str, stopwords_set: set):
    """
    Processes scraped text by dropping stop words & indexing text
    input: raw_text: string of text returned from webscraper
    input: stopwords_set: set of English stopwords to be dropped from raw text
    output: out_text
    """


