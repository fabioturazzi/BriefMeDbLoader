import scraper_cnn
import scraper_cbc
import scraper_bbc
import scraper_globalnews
import scraper_ap
import scraper_npr
import scraper_nationalpost
import scraper_businessinsider
import scraper_abcnews
import scraper_cnbc
import pymongo
import pandas as pd
from datetime import datetime
import summarize_text_bart

while True:

    start = datetime.now()

    # Call scraper methods to fetch all articles
    articles_cnn = scraper_cnn.scrape_cnn(15)
    articles_cbc = scraper_cbc.scrape_cbc(15)
    articles_bbc = scraper_bbc.scrape_bbc(15)
    articles_npr = scraper_npr.scrape_npr(15)
    articles_globalnews = scraper_globalnews.scrape_globalnews(25)
    articles_abc = scraper_abcnews.scrape_abc(15)

    # articles_ap = scraper_ap.scrape_ap(15)
    # articles_nationalpost = scraper_nationalpost.scrape_nationalpost(15)
    # articles_businessinsider = scraper_businessinsider.scrape_businessinsider(15)
    # articles_cnbc = scraper_cnbc.scrape_cnbc(15)

    #Assign all sources to an array
    article_all_sources = [articles_abc, articles_npr, articles_cnn, articles_cbc, articles_bbc, articles_globalnews]

    #Print amount of articles scraped
    print("CNN", len(articles_cnn))
    print("CBC", len(articles_cbc))
    print("BBC", len(articles_bbc))
    print("GlobalNews", len(articles_globalnews))
    print("NPR", len(articles_npr))
    print("ABC", len(articles_abc))

    # print("AP News", len(articles_ap))
    # print("National post", len(articles_nationalpost))
    # print("Business insider", len(articles_businessinsider))
    # print("CNBC", len(articles_cnbc))

    # Start mongo connection
    client = pymongo.MongoClient("mongodb+srv://briefme:briefmeapp@briefmecluster.ylnmc.mongodb.net/briefmedb?retryWrites=true&w=majority")
    mydb = client["briefmedb"]
    mycol = mydb["articles"]

    #Loop through the array of arrays, containing sets of articles from each source
    for articles in article_all_sources:
        try:
            print("Summarizing: ", articles[0]['source'])
            #Assign array of dictionaries to a dataframe
            df = pd.DataFrame.from_dict(articles)
            #Remove duplicates and NaN values
            df = df.drop_duplicates()
            df = df.dropna(subset=['description'])
            df = df.dropna(subset=['title'])

            #Dropping articles with less than 200
            df = df[df['description'].apply(lambda x: len(str(x))) > 200]

            #Apply summarizer to the article
            df['summary'] = df['description'].apply(lambda x: summarize_text_bart.summarize_bart(x))

            #Delete previous articles from that source and add new articles
            clear = mycol.delete_many({"source": articles[0]['source']})
            repopulate = mycol.insert_many(df.to_dict('records'))
        except:
            print("Unable to save articles from source")



    #Print time the application finished loading a batch of articles
    now = datetime.now()
    print("Start - ", start.strftime("%m/%d/%Y, %H:%M:%S") )
    print("End - ", now.strftime("%m/%d/%Y, %H:%M:%S") )