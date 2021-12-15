from matplotlib import pyplot as plt
from PIL import Image, ImageFont, ImageDraw
import collections

def update_plots(analytics_data):
    """
    Main function to do all the plots for the dashboard
    """
    for i in range(7):
        do_plot(analytics_data, i)

def do_plot(analytics_data, i):
    """
    Function for doing each individual plots
    """
    if i == 0:  # Clicks on document per rank:
        ranks = []
        for click in analytics_data.fact_clicks:
                ranks.append(click.rank)

        ranks_count = collections.Counter(ranks)
        plt.bar(ranks_count.keys(),ranks_count.values())
        plt.xlabel("Rank")
        plt.ylabel("Count")
        plt.savefig("static/plot_1.png")
        plt.figure()

    elif i == 1:  # Number of sent queries

        n_queries = len(analytics_data.fact_queries)

        img = Image.new('RGB', (500, 500), (250, 250, 250))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("OpenSans-Regular.ttf", 400)
        draw.text((150, -30), str(n_queries), (0, 0, 0), font=font)
        img.save('static/plot_2.png')

    elif i == 2:  # Platforms used:

        platforms = []
        for user in analytics_data.fact_users.values():
            platforms.append(user.platform)

        platforms_count = collections.Counter(platforms)
        plt.bar(platforms_count.keys(), platforms_count.values())
        plt.xlabel("Platform")
        plt.ylabel("Count")
        plt.savefig("static/plot_3.png")
        plt.figure()

    elif i == 3:  # Browsers used:
        browsers = []
        for user in analytics_data.fact_users.values():
            browsers.append(user.browser)

        browsers_count = collections.Counter(browsers)
        plt.bar(browsers_count.keys(), browsers_count.values())
        plt.xlabel("Browser")
        plt.ylabel("Count")
        plt.savefig("static/plot_4.png")
        plt.figure()

    elif i == 4:  # Most popular queries:
        queries = []
        for query in analytics_data.fact_queries:
            queries.append(query.text)

        queries_count = collections.Counter(queries)
        plt.bar(queries_count.keys(), queries_count.values())
        plt.xlabel("Query")
        plt.ylabel("Count")
        plt.savefig("static/plot_5.png")
        plt.figure()

    elif i == 5:  # How many terms per query
        terms = []
        for query in analytics_data.fact_queries:
            terms.append(query.n_terms)

        terms_count = collections.Counter(terms)
        plt.bar(terms_count.keys(), terms_count.values())
        plt.xlabel("Terms")
        plt.ylabel("Count")
        plt.savefig("static/plot_6.png")
        plt.figure()

    else:  # Document analysis
        docs = {"clicks": {}, "ranks":{}, "times":{}}
        for doc in analytics_data.fact_documents.values():
            doc_id = doc.doc_id
            if doc.n_clicks >0:
                docs["clicks"][doc_id] = doc.n_clicks
            if doc.ranking_clicked is not None:
                docs["ranks"][doc_id] = doc.ranking_clicked
            if doc.dwell_time is not None:
                docs["times"][doc_id] = doc.dwell_time

        # Sorting docs
        docs["clicks"] = {k: v for k, v in sorted(docs["clicks"].items(), key=lambda item: item[1],reverse=True)}
        docs["ranks"] = {k: v for k, v in sorted(docs["ranks"].items(), key=lambda item: item[1],reverse=True)}
        docs["times"] = {k: v for k, v in sorted(docs["times"].items(), key=lambda item: item[1],reverse=True)}

        # Plotting
        plt.bar(docs["clicks"].keys(), docs["clicks"].values())
        plt.xlabel("Document")
        plt.ylabel("Clicks")
        plt.savefig("static/plot_7.png")
        plt.figure()
        plt.bar(docs["ranks"].keys(), docs["ranks"].values())
        plt.xlabel("Document")
        plt.ylabel("Avg. Clicked Rank")
        plt.savefig("static/plot_8.png")
        plt.figure()
        plt.bar(docs["times"].keys(), docs["times"].values())
        plt.xlabel("Document")
        plt.ylabel("Avg. Dwell Time")
        plt.savefig("static/plot_9.png")




