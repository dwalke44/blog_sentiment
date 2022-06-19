import string
import re
import numpy as np
from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences


class Vectorizer:
    def __init__(self):
        self.inverse_vocabulary = None
        self.vocabulary = None

    def standardize(self, text):
        text = text.lower()
        return "".join(char for char in text if char not in string.punctuation)

    def tokenize(self, text):
        text = self.standardize(text)
        return text.split()

    def make_vocabulary(self, dataset):
        self.vocabulary = {"": 0, "[UNK]": 1}
        for text in dataset:
            text = self.standardize(text)
            tokens = self.tokenize(text)
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary[token] = len(self.vocabulary)
        self.inverse_vocabulary = dict(
            (v, k) for k, v in self.vocabulary.items())

    def encode(self, token_list):
        return [self.vocabulary.get(token, 1) for token in token_list]

    def decode(self, int_sequence):
        return " ".join(
            self.inverse_vocabulary.get(i, "[UNK]") for i in int_sequence)


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
            if re.sub("\d+", "", word) not in punctuation:
                word_tokens.append(word)

    # Filter out drop words
    filtered_text = []
    for w in word_tokens:
        if w.lower() not in stopwords_set:
            filtered_text.append(w)

    return filtered_text


def sort_filtered_text(filtered_text, desired_len):
    """
    Arranges filtered tokens & returns {desired_len} most occurring tokens
    """
    desired_len = int(desired_len)
    count = Counter(filtered_text).most_common(n=desired_len)

    return count


def convert_samples_to_model_input(cleaned_samples, counter_vocabulary, seq_len=300):
    """
    Converts tokenized blog texts to updated vocabulary and integer array representing blogs
    input: cleaned_samples: pd.DataFrame of one blog post per row, single string of cleaned tokens
    input: counter_vocabulary: Counter() object of vocabulary
    input: seq_len: required length of integers per sample
    output: vocab: updated Counter() object dictionary of words & their number of occurrences
    output: sequences: ndarray of converted text to integers
    """
    vocab = counter_vocabulary
    for k in np.arange(0, cleaned_samples.shape[0]):
        text = cleaned_samples[0][k]
        vocab.update(text.split())
    # Create mapping from counter
    word_counts = sorted(vocab, key=vocab.get, reverse=True)

    # Produce ranks of words by occurrence, defining their int representation
    word_to_int = {word: ii for ii, word in enumerate(word_counts, 1)}

    # Map each blog sample from words to int using dictionary produced in prev step
    mapped_text = []
    for m in cleaned_samples.iloc[:, 0]:
        mapped_text.append([word_to_int[word] for word in m.split()])

    # Left pad integer sequences
    sequences = np.zeros((len(mapped_text), seq_len), dtype=int)
    for n, row in enumerate(mapped_text):
        text_arr = np.array(row)
        sequences[n, -len(row):] = text_arr[-seq_len:]

    return vocab, sequences

# def standardize_token_sequences(token_list, desired_len):
#     """
#     Takes clean list of tokens & converts to integer, pads to desired length
#     """
#     desired_len = int(desired_len)
#     t = Tokenizer(num_words=desired_len)
#     t.fit_on_texts(token_list)
#     sequence = t.texts_to_sequences(token_list)
#     word_index = t.word_index
#     output = pad_sequences(sequence, maxlen=desired_len)
#     v = Vectorizer()
#     v.make_vocabulary(dataset=token_list)
#     enc = v.encode(token_list=token_list)
#     return word_index, output
