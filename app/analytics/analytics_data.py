# Analytics main Data Structure
class AnalyticsData:

    def __init__(self):
        self.fact_clicks = []
        self.fact_queries = []
        self.fact_documents = {}
        self.fact_users = {}

    # Add new click to analytics
    def new_click(self, doc_id, date, rank):
        self.fact_clicks.append(Click(doc_id, date, rank))
        self.fact_documents[doc_id].clicked(rank)

    # Add new query to analytics
    def new_query(self, text, n):
        self.fact_queries.append(Query(text, n))

    # Add new session to analytics
    def new_session(self, ip, platform, browser, language, time):
        if ip not in self.fact_users.keys():
            self.fact_users[ip] = User(ip, platform, browser, language, time)
        else:
            self.fact_users[ip].new_log(time)

    # Add new user to analytics
    def new_user(self, ip, platform, browser, language, time):
        self.fact_users[ip] = User(ip, platform, browser, language, time)

    # Update analytics for a single doc
    def update_doc(self, doc_id, query, ranking):
        if doc_id not in self.fact_documents.keys():
            self.fact_documents[doc_id] = Document(doc_id, query, ranking)
        else:
            self.fact_documents[doc_id].update(query, ranking)

    # New dwell time for a single doc
    def new_dwell(self, doc_id):
        self.fact_documents[doc_id].new_dwell()

    # Update las dwell time for a single dwell time
    def update_dwell_time(self,doc_id, dwell_time):
        self.fact_documents[doc_id].update_dwell_time(dwell_time)


# Data Structure for Clicks
class Click:
    def __init__(self,doc_id,date,rank):
        self.doc_id = doc_id
        self.date = date
        self.rank = rank

# Data Structure for Query
class Query:
    def __init__(self, text, n):
        self.text = text
        self.n_terms = len(text.split())
        self.n_query = n

# Data Structure for Document
class Document:
    def __init__(self, doc_id, query, ranking):
        self.doc_id = doc_id
        self.queries = [query]
        self.rankings = [ranking]
        self.ranking = ranking
        self.rankings_clicked = []
        self.ranking_clicked = None
        self.dwell_times = []
        self.dwell_time = None
        self.n_clicks = 0

    def update(self, query, ranking):
        self.queries.append(query)
        self.rankings.append(ranking)
        self.ranking = sum(self.rankings)/len(self.rankings)

    def clicked(self, ranking):
        self.n_clicks+=1
        self.rankings_clicked.append(ranking)
        self.ranking_clicked = sum(self.rankings_clicked)/len(self.rankings_clicked)

    def new_dwell(self):
        self.dwell_times.append(0)

    def update_dwell_time(self,dwell_time):
        self.dwell_times[-1] = dwell_time
        self.dwell_time = sum(self.dwell_times)/len(self.dwell_times)

# Data Structure for User
class User:
    def __init__(self, ip, platform, browser, language, time):
        self.ip = ip
        self.platform = platform
        self.browser = browser
        self.language = language
        self.time_logs = [time]

    def new_log(self, time):
        self.time_logs.append(time)