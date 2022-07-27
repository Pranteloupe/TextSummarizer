import numpy as np
from nltk.cluster.util import cosine_distance

def sentence_similarity(sentence1, sentence2, stopwords=None):
    if stopwords == None:
        stopwords = []

    sentence_array1 = []
    for w in sentence1:
        sentence_array1.append(w.lower())
    sentence_array2 = []
    for w in sentence2:
        sentence_array2.append(w.lower())

    all_words = list(set(sentence_array1 + sentence_array2))

    vect1 = [0] * len(all_words)
    vect2 = [0] * len(all_words)

    for w in sentence_array1:
        if w in stopwords:
            continue
        vect1[all_words.index(w)] += 1
    
    for w in sentence_array2:
        if w in stopwords:
            continue
        vect2[all_words.index(w)] += 1

    return 1 - cosine_distance(vect1, vect2)

def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for index1 in range(len(sentences)):
        for index2 in range(len(sentences)):
            if index1 == index2:
                continue
            similarity_matrix[index1][index2] = sentence_similarity(sentences[index1], sentences[index2], stop_words)

    return similarity_matrix
