import string
from nltk.tokenize import word_tokenize, sent_tokenize
from keras.preprocessing.text import Tokenizer


def word_token_drop_sw(raw_text: str, stopwords_set: set):
    """
    Processes scraped text by dropping stop words & indexing text
    input: raw_text: string of text returned from webscraper
    input: stopwords_set: set of English stopwords to be dropped from raw text
    output: out_text
    """
    # Base punctuation list missing an ’ so add that to filter list
    punctuation = string.punctuation + "’"

    # Tokenize text into sentences
    sent_tokens = sent_tokenize(raw_text)

    # Tokenize sentences into words & drop punctuation
    word_tokens = []
    word_tokens_int = []
    for sent in sent_tokens:
        words = word_tokenize(sent)
        word_tokens_int.append(words)
        # print(word_tokens_int)
    for sent in word_tokens_int:
        for word in sent:
            if word not in punctuation:
                word_tokens.append(word)

    # Filter out drop words
    filtered_text = []
    for w in word_tokens:
        if w.lower() not in stopwords_set:
            filtered_text.append(w)

    return filtered_text


def prep_tokens_for_embed(token_list, desired_len):
    """
    Takes clean list of tokens & converts to integer, pads to desired length
    """
    t = Tokenizer(num_words=desired_len)

