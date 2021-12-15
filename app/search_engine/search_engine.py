import random

from app.search_engine.algorithms import search_tf_idf_custom
from app.core.utils import load_documents_corpus, parseTweet


class SearchEngine:
    """educational search engine"""

    def __init__(self, tweets, index, tf, idf):
        self.tweets= tweets
        self.index = index
        self.tf = tf
        self.idf = idf

    def search(self, search_query):
        print("Search query:", search_query)
        results = search_tf_idf_custom(search_query, self.tweets, self.index, self.tf, self.idf)
        results = self.format_results(results)

        return results

    def format_results(self,results):
        new_results = []
        for ranking, tweet_id in enumerate(results):
            tweet = self.tweets[str(tweet_id)]
            new_results.append(parseTweet(tweet, tweet_id, ranking+1))
        return new_results

