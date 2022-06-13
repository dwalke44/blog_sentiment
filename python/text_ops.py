import string
from nltk.tokenize import word_tokenize, sent_tokenize
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences


class Vectorizer:
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

    def encode(self, text):
        text = self.standardize(text)
        tokens = self.tokenize(text)
        return [self.vocabulary.get(token, 1) for token in tokens]

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
            if word not in punctuation:
                word_tokens.append(word)

    # Filter out drop words
    filtered_text = []
    for w in word_tokens:
        if w.lower() not in stopwords_set:
            filtered_text.append(w)

    return filtered_text


def standardize_token_sequences(token_list, desired_len):
    """
    Takes clean list of tokens & converts to integer, pads to desired length
    """
    t = Tokenizer(num_words=desired_len)
    t.fit_on_texts(token_list)
    sequence = t.texts_to_sequences(token_list)
    word_index = t.word_index
    output = pad_sequences(sequence, maxlen=desired_len)

    return word_index, output
