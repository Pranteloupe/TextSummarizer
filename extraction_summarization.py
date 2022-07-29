import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('word_tokenize')

def create_dictionary(text_string) -> dict:

    nltk.download('stopwords')

    #Create the list of stopwords
    stop_words = stopwords.words('english')

    #A porter stemmer reduces words to their root form
    stemmer = PorterStemmer()

    #Tokenize text into separate words
    words = []
    for sentence in text_string:
        words += word_tokenize(sentence)
   # words = word_tokenize(text_string)

    frequency_table = dict()
    for word in words:
        word = stemmer.stem(word) 
        if word in stop_words: 
            continue
        if word in frequency_table: #Increment word in dictionary by one
            frequency_table[word] += 1
        else:
            frequency_table[word] = 1 
    
    return frequency_table

def calculate_scores(sentences, frequency_table):

    sentence_score = dict() 

    #nltk.download('word_tokenize')

    for sentence in sentences:
        sentence_without_stopwords = 0
        for word_score in frequency_table:
            if word_score in sentence:
                sentence_without_stopwords += 1
                if sentence in sentence_score: #Using the first 12 characters in the sentence to search in sentence_score
                    sentence_score[sentence] += frequency_table[word_score]
                else:
                    sentence_score[sentence] = frequency_table[word_score]
        #sentence_score[sentence] = (sentence_score[sentence] / sentence_without_stopwords)  #Dividing sentence by the number of words

    return sentence_score

def get_summary(sentences, sentence_score, threshold):
    sent_count = 0
    summary = ''

    for sentence in sentences:
        if sentence in sentence_score and sentence_score[sentence] >= threshold:
            summary += " " + sentence
            sent_count += 1

    return summary