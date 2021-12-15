import nltk
from flask import Flask, render_template, request
from flask import request

from app.analytics.analytics_data import AnalyticsData
from app.core.utils import load_documents_corpus, parseTweet
from app.search_engine.search_engine import SearchEngine
import time
from app.core.plots import update_plots
from datetime import datetime


app = Flask(__name__)

analytics_data = AnalyticsData()
tweets, index, tf, idf = load_documents_corpus()
searchEngine = SearchEngine(tweets, index, tf, idf)

## Global variables: ##
last_clicked_doc = None  # To know the last clicked document (if any), for computing dwell time
n_queries=0  # Total number of queries executed


@app.route('/')
def search_form():
    global last_clicked_doc  # Global variable used
    last_clicked_doc = None  # Reseting timers, if any

    # Updating User table
    user_ip = request.remote_addr
    user = request.user_agent
    analytics_data.new_session(user_ip, user.platform, user.browser, user.language, datetime.now(), )

    return render_template('index.html', page_title="Welcome")


@app.route('/search', methods=['POST','GET'])
def search_form_post():
    global last_clicked_doc  # Global variable used
    global n_queries  # Global variable used
    n_queries += 1

    # If we come from a document, update the dwell time
    try:
        from_document = bool(request.args["from-document"])
        search_query = request.args["search-query"]
        doc_id = last_clicked_doc[0]
        dwell_time = time.time() - last_clicked_doc[1]
        analytics_data.update_dwell_time(doc_id, dwell_time)
    except:
        from_document = None
        search_query = request.form["search-query"]

    # Computing results using our algorithm
    results = searchEngine.search(search_query)
    found_count = len(results)

    # Saving statistics (only if we don't come from a document)
    if not from_document:
        # Updating Query table
        analytics_data.new_query(search_query, n_queries)
        for ranking, result in enumerate(results):
            analytics_data.update_doc(result.id, search_query, ranking+1)

    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count, query=search_query)


@app.route('/doc_details', methods=['GET','POST'])
def doc_details():
    global last_clicked_doc  # Global variable used

    # Updating Click table
    clicked_doc_id = request.args["id"]
    last_clicked_doc = (clicked_doc_id, time.time())  # For later computing of dwell time
    click_date = datetime.now()
    click_rank = int(request.args["rank"])
    analytics_data.new_click(clicked_doc_id, click_date, click_rank)

    #Obtaining the document object
    document = parseTweet(tweets[clicked_doc_id], clicked_doc_id, click_rank)

    # Restarting the timer for computing dwell time later
    analytics_data.new_dwell(clicked_doc_id)
    query = request.args["query"]
    last_clicked_doc = (clicked_doc_id, time.time())

    return render_template('doc_details.html',page_title="Document Details",doc=document, query=query)


@app.route('/stats', methods=['GET'])
def analytics():
    """
    Dashboard
    """
    update_plots(analytics_data)  # Generating plots in computer
    return render_template('dashboard.html')

@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port="8088", host="0.0.0.0", threaded=False, debug=True)
