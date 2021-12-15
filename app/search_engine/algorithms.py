from app.core.utils import build_terms, to_datetime, parse_date
import collections
from collections import defaultdict
import numpy as np


def time_decay(days, half_life):
    tau = half_life/np.log(2)
    return np.exp(-days/tau)

def social_score(tweets, tweet_id, rt_weight=2 / 3):
    # We compute the social score for a tweet
    tweet = tweets[tweet_id]
    favs = int(tweet["favorite_count"])
    retweets = int(tweet["retweet_count"])

    score = rt_weight * retweets + (1 - rt_weight) * favs

    return score


def decay_score(tweets, tweet_id, half_life=15):
    # Decay score for a tweet
    return time_decay(parse_date(tweets[tweet_id]["created_at"]), half_life)


def total_score(tf_idf_score, social_score, decay_score, social_score_weight=0.3):
    """
    Computes the final score for a document

    Argument
    tf_idf_score: classic tf_idf document score
    social_score. social score for the document, based on number of likes and rt's
    decay_score: coefficient accounting for the decay of relevance over time
    social_score_weight: Ponders relative importance of the social score over the tf_idf score

    Returns:
    The final score for a given document
    """
    return decay_score * (social_score * social_score_weight + tf_idf_score)


def rank_documents_custom(terms, docs, tweets, index, idf, tf):
    """
    Perform the ranking of the results of a search based on the tf-idf weights

    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies

    Returns:
    Print the list of ranked documents
    """

    # I'm interested only on the element of the docVector corresponding to the query terms
    # The remaining elements would became 0 when multiplied to the query_vector
    doc_vectors = defaultdict(lambda: [0] * len(
        terms))  # I call doc_vectors[k] for a nonexistent key k, the key-value pair (k,[0]*len(terms)) will be automatically added to the dictionary
    query_vector = [0] * len(terms)

    # compute the norm for the query tf
    query_terms_count = collections.Counter(terms)  # get the frequency of each term in the query.

    query_norm = sum(query_terms_count.values())

    for termIndex, term in enumerate(terms):  # termIndex is the index of the term in the query
        if term not in index:
            continue

        ## Compute tf*idf(normalize TF as done with documents)
        query_vector[termIndex] = query_terms_count[term] / query_norm * idf[term]

        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):
            if doc in docs:
                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term]  # TODO: check if multiply for idf

    # Calculate the score of each doc
    # SEE THE REPORT FOR MORE INFORMATION ON THIS FORMULA!
    doc_scores = [
        [total_score(np.dot(curDocVec, query_vector), social_score(tweets, str(doc)), decay_score(tweets, str(doc))),
         doc] for doc, curDocVec in doc_vectors.items()]
    doc_scores.sort(reverse=True)
    result_docs = [x[1] for x in doc_scores]

    return result_docs


def search_tf_idf_custom(query, tweets, index, tf, idf):
    """
    output is the list of documents that contain ALL the query terms (WE ARE DEALING WITH CONJUCTIVE QUERIES)
    So, we will get the list of documents for each query term, and take the union of them.
    """
    query = build_terms(query)
    docs = set()
    for i, term in enumerate(query):
        if term in index.keys():

            # store in term_docs the ids of the docs that contain "term"
            term_docs = set([posting[0] for posting in index[term]])

            # If it's the first term:
            if i == 0:
                docs = term_docs

            else:
                docs = docs.intersection(term_docs)

        else:
            docs = set()
            break

    docs = list(docs)
    ranked_docs = rank_documents_custom(query, docs, tweets, index, idf, tf)
    return ranked_docs