# BriefMeDbLoader
## A Web Application that delivers summarized news articles

## Overview:

[BreifMe](https://briefmenews.herokuapp.com/) full project consists of [BriefMeDbLoader repo](https://github.com/fabioturazzi/BriefMeDbLoader) as the backend, responsible for obtaining data and preparing it for the web application, and [BriefMe repo](https://github.com/fabioturazzi/BriefMe) and the frontend, reponsible for displaying contents and supporting functions to help filtering news and listening to news.  

**Method:** Web Contents Scraping, Text Summarization with Transformers

**Tools:** Pycharm Project
- Web Scraping: [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [requests-html](https://pypi.org/project/requests-html/)
- Summarization: [PyTorch](https://pytorch.org/), [Transformers](https://huggingface.co/transformers/), [BART](https://huggingface.co/transformers/model_doc/bart.html)
- Additional utilities: [pandas](https://pandas.pydata.org/docs/index.html), [PyMongo](https://pymongo.readthedocs.io/en/stable/)

## Project Motivations:
This is an academic project developed by Fabio Turazzi and Do Man Uyen Nguyen, proposing a solution for those who wish to keep themselves up to date on the latest news. Considering the growth in use of social media to access news and the growing threat of fake news in those media, our goal was to develop a platform that offers consolidated information from credible sources, while maintaining the practicality sought-after in social media.

This application applies Web Scraping techniques to consolidate articles from sources such as BBC, CNBC, CNN, among others. Additionally, it differentiates itself from other news compilers by applying Natural Language Processing techniques to summarize those articles, offering quick briefings for users. Combining these two factors, we believe that we offer a better way for users to efficiently browse articles, while providing links to the full articles for those who wish to obtain more detailed information.

**Disclaimer: This application was developed for study purposes and is not intended for commercial use.**

## Functionality

This Database Loader is responsible for gathering necessary information to display on our web application. 

Its three main funtions are: scraping news articles from news websites using customized scripts, applying a BART pre-trained summarization algorithm on the obtained articles to produce their corresponding summaries, and storing the information in MongoDB Atlas for retrieval. 

## Directory
```
|- CSIS4495_BriefMe_DbLoader
| -- summarizer
|   --- __init__.py                             Empty init file for import
|   --- summarize_text_bart.py                  Script to summarize text using pretrained BART
| -- web_scrapers
|   --- __init__.py                             Empty init file for import
|   --- scraper_abcnews.py                      Script to scrape ABC News
|   --- scraper_ap.py                           Script to scrape AP News
|   --- scraper_bbc.py                          Script to scrape BBC News
|   --- scraper_businessinsider.py              Script to scrape Business Insider News
|   --- scraper_cbc.py                          Script to scrape CBC News
|   --- scraper_cnbc.py                         Script to scrape CNBC News
|   --- scraper_cnn.py                          Script to scrape CNN News
|   --- scraper_globalnews.py                   Script to scrape Global News
|   --- scraper_nationalpost.py                 Script to scrape National Post News
|   --- scraper_npr.py                          Script to scrape NPR News
| -- error.log                                  Log errors for debugging
| -- main.py                                    Main script to run the program that calls scraping scripts and summarizing script, save the data into MongoDB Atlas cluster
| -- main_single.py                             Main script to run the program that calls a single scraping script and summarizing script, for debugging 
| -- README.md                                  Overview information

```

## Challenges:
Considering the large amount of articles (about 400 articles), applying BART summarization on all of them systematically is extremely time-consuming, thus, is not desirable for the scope of our project. As the result, we excluded some scraping scripts and put a cap on the number of articles in order to alleviate the updating time.  

While attempting to re-train the pre-trained BART model, we encountered the limited processing power issue, even though we succeeded in following [ohmeow-blurr](https://github.com/ohmeow/ohmeow_website/blob/master/_notebooks/2020-05-23-text-generation-with-blurr.ipynb) guide to  construct a BartForConditionalGeneration object to train a small fraction of [*cnn_dailymail* dataset](https://www.tensorflow.org/datasets/catalog/cnn_dailymail). Therefore, we moved forward with the pre-trained model for the final output. 

Another consideration during the research for deployment the Pycharm project involved running an EC2 instance on AWS indefinitely so that the website would always display the latest articles. By using [AWS toolkit](https://aws.amazon.com/pycharm/) extension for Pycharm, we were able to connect to a running EC2 instance, upload all the files and download the requirements to the remote machine. Nevertheless, the free-tier machine could not handle the task because of the overdemanding processing. 

## Future considerations:
There are several alternatives that we believe would improve the performance by addressing the aforementioned issues.

Most of the problems can be ameliorated by utilizing stronger computational resources, which have enough power to accelerate the execution time and handle heavy processing demands, for example experiencing with Hadoop and Spark. 

In order to produce the highest quality summaries, it would be ideal to use a customized dataset with articles and their corresponding summaries in order to retrain BART with better computational power machine. 
