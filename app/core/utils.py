import datetime
from random import random

import json
from collections import defaultdict
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from num2words import num2words
import re
import string
from array import array
import math
import numpy as np
from datetime import datetime, timedelta
from email.utils import parsedate_tz
nltk.download('stopwords')


#From string retrieved by twitter to datetime object
def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])

#The most recent date for a tweet. To measure the days passed from last to most recent
last = "Wed Oct 13 09:15:58 +0000 2021"
last_date = to_datetime(last)

#From a date to days elapsed, starting at the latest tweet
def parse_date(date):
    date = to_datetime(date)
    return abs((last_date - date).days)

#Function to assess whether a string is a number or not
def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# Function to remove emojis from a text
def remove_emojis(data):
    """
    Removes all emojis from a string of text
    """
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def build_terms(tweet):
    """
    Preprocess the article text (title + body) removing stop words, stemming,
    transforming in lowercase and return the tokens of the text.

    Argument:
    line -- string (text) to be preprocessed

    Returns:
    line - a list of tokens corresponding to the input text after the preprocessing
    """

    # Removing links
    tweet = tweet.split()
    tweet = ' '.join([word for word in tweet if "http" not in word])

    # removing emojis
    tweet = remove_emojis(tweet)

    # Detecting hashtags
    tweet = re.sub(r"(\s|^)\#(\S)", r"\1 hashtag \2", tweet)
    tweet = re.sub(r"(\s|^)\@(\S)", r"\1 atsign \2", tweet)

    punctuation_marks = set(string.punctuation + "…" + "’" + "“" + "”") - set([".", "-", "/", "%", "$", "\n"])
    tweet = ''.join(ch for ch in tweet if ch not in punctuation_marks)

    # we just replace any slash to a white space.
    tweet = re.sub("/", " ", tweet)

    # We replace any point placed at the end of a number into a white space (if we didn't do so, we would have problems in the "num2words" step)
    tweet = re.sub(r"(\d)\.(\D)", r"\1 \2", tweet)

    # Replacing any quantity with the dollar sign to the quantity followed by the word "dollars".
    tweet = re.sub(r'\$([0-9]+\.?[0-9]*)', '\g<1> dollars', tweet)

    # Replacing any "%" sign to the word "percent"
    tweet = re.sub("%", " percent", tweet)

    # Replacing any "-" sign to a white space
    tweet = re.sub(r"[-–]", " ", tweet)

    # Any quantity followed by "s" is now followed by the "seconds" word (instead of the "s" char)
    tweet = re.sub(r"(\d)s", r"\1 seconds", tweet)

    # "Num2words" step. We iterate through every word of the current text and we check if the word is actually a number (by using
    # the function defined above). If it is a number, we replace it by its word representation. If not, we just leave it as it is.
    words = tweet.split(" ")
    tweet = ""
    for word in words:
        if is_number(word):
            try:
                word = num2words(float(word))
            except:
                print("Error trying to transform " + str(word) + " into number")
        tweet += word + " "

        # After converting numbers to words, commas and hyphens can appear again, so we have to remove them with the same code used before
    tweet = re.sub(r"[-–]", " ", tweet)
    tweet = re.sub(",", "", tweet)

    # After converting numbers to words, we can also remove all the remaining dots
    tweet = ''.join(ch for ch in tweet if ch != ".")

    # If we had more than one consecutive white space, we replace it by a single one
    tweet = re.sub(' +', ' ', tweet)

    # Transform WHO to World Health Organization
    tweet = tweet.split()
    tweet = ["WORLD" if word == "W" else word for word in tweet]
    tweet = ["HEALTH" if word == "H" else word for word in tweet]
    tweet = " ".join(["ORGANIZATION" if word == "O" else word for word in tweet])

    # converting all the characters to lowercase
    tweet = tweet.lower()

    # removing stop words
    tweet = tweet.split()
    stop_words = set(stopwords.words("english"))
    tweet = [word for word in tweet if word not in stop_words]  ##eliminate the stopwords

    # stemming
    stemmer = PorterStemmer()
    tweet = [stemmer.stem(word) for word in tweet]  ## perform stemming

    ## END CODE
    return tweet

def create_index_tfidf(tweets, num_tweets):
    """
    Implement the inverted index and compute tf, df and idf

    Argument:
    lines -- collection of Wikipedia articles
    num_documents -- total number of documents

    Returns:
    index - the inverted index (implemented through a Python dictionary) containing terms as keys and the corresponding
    list of document these keys appears in (and the positions) as values.
    tf - normalized term frequency for each term in each document
    df - number of documents each term appear in
    idf - inverse document frequency of each term
    """

    index = defaultdict(list)
    tf = defaultdict(list)  # term frequencies of terms in documents (documents in the same order as in the main index)
    df = defaultdict(int)  # document frequencies of terms in the corpus
    idf = defaultdict(float)

    for tweet_id, tweet in enumerate(tweets):

        text = tweet["full_text"]

        terms = build_terms(text)

        ## ===============================================================
        ## create the index for the **current page** and store it in current_page_index
        ## current_page_index ==> { ‘term1’: [current_doc, [list of positions]], ...,‘term_n’: [current_doc, [list of positions]]}

        ## Example: if the curr_doc has id 1 and his text is
        ##"web retrieval information retrieval":

        ## current_page_index ==> { ‘web’: [1, [0]], ‘retrieval’: [1, [1,4]], ‘information’: [1, [2]]}

        ## the term ‘web’ appears in document 1 in positions 0,
        ## the term ‘retrieval’ appears in document 1 in positions 1 and 4
        ## ===============================================================

        current_page_index = {}

        for position, term in enumerate(terms):  ## terms contains page_title + page_text
            try:
                # if the term is already in the dict append the position to the corresponding list
                current_page_index[term][1].append(position)
            except:
                # Add the new term as dict key and initialize the array of positions and add the position
                current_page_index[term] = [tweet_id,
                                            array('I', [position])]  # 'I' indicates unsigned int (int in Python)

        # normalize term frequencies
        # Compute the denominator to normalize term frequencies (formula 2 above)
        # norm is the same for all terms of a document.
        norm = 0
        for term, posting in current_page_index.items():
            # posting will contain the list of positions for current term in current document.
            # posting ==> [current_doc, [list of positions]]
            # you can use it to infer the frequency of current term.
            norm += len(posting[1]) ** 2
        norm = math.sqrt(norm)

        # calculate the tf(dividing the term frequency by the above computed norm) and df weights
        for term, posting in current_page_index.items():
            # append the tf for current term (tf = term frequency in current doc/norm)
            tf[term].append(np.round(len(posting[1]) / norm, 4))  ## SEE formula (1) above
            # increment the document frequency of current term (number of documents containing the current term)
            df[term] += 1  # increment DF for current term

        # merge the current page index with the main index
        for term, positions in current_page_index.items():
            index[term].append(positions)

        # Compute IDF following the formula (3) above. HINT: use np.log
        for term in df:
            idf[term] = np.round(np.log(float(num_tweets / df[term])), 4)

    return index, tf, idf


def load_documents_corpus():
    """
    Load documents corpus from dataset_tweets_WHO.txt file
    :return: tf-idf index (including tf df and idf scores)
    """

    ##### demo replace ith your code here #####
    docs_path = 'dataset_tweets_WHO.txt'

    dictionary = []
    with open(docs_path) as fp:
        tweets = json.loads(fp.read())

    num_documents = len(tweets)
    index, tf, idf = create_index_tfidf(tweets.values(), num_documents)
    return tweets, index, tf, idf

def parseTweet(tweet,tweet_id,ranking):
    """
    Function to parse a tweet to a DocumentInfo object
    """
    text = tweet["full_text"]
    username = tweet["user"]["name"]
    date = tweet["created_at"]
    hashtags = tweet["entities"]["hashtags"]
    favs = tweet["favorite_count"]
    retweets = tweet["retweet_count"]
    url = "https://twitter.com/" + tweet["user"]["screen_name"] + "/status/" + tweet["id_str"]
    return DocumentInfo(tweet_id, text, username, date, hashtags, favs, retweets, url, ranking)

class DocumentInfo:
    """
    DocumentInfo class, to store tweet relevant information
    """
    def __init__(self, id, text, username, date, hashtags, favs, retweets, url, ranking):
        self.id = str(id)
        self.username = username
        self.title = username+": " + text[:20] + "..."
        self.description = text
        self.doc_date = date
        self.url = url
        self.ranking = str(ranking)
        self.favs = favs
        self.retweets = retweets
        self.hashtags = hashtags