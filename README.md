# BriefMeDbLoader
## A Web Application that delivers summarized news articles

## Overview:

[BriefMe](https://briefmenews.herokuapp.com/) full project consists of:
- [BriefMeDbLoader repo](https://github.com/fabioturazzi/BriefMeDbLoader) - a PyCharm program responsible for scraping articles from the web, summarizing them, and loading a MongoDB database, and 
- [BriefMe repo](https://github.com/fabioturazzi/BriefMe) - Node.js web application, reponsible for pulling article contents from the database and displaying it on the website, as well as supporting additional functions to help filtering and listening to news.  

**Method:** Web Content Scraping, Text Summarization with Transformers

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
| -- project_report
|   --- BriefMe - Project Report.pdf            Complete report describing project development process
| -- error.log                                  Log errors for debugging
| -- main.py                                    Main script to run the program, continuously calls scraping/summarizing scripts and saves the data into MongoDB Atlas cluster
| -- main_single.py                             Alternative to main script which executes a single instance of the scraping and summarizing scripts, used for debugging 
| -- README.md                                  Overview information

```

## Challenges:
Considering the large amount of articles (about 400 articles), applying BART summarization on all of them systematically is extremely time-consuming, thus, is not desirable for the scope of our project. As the result, we opted to limit the scope of the project to a smaller sample of sources and articles. The unconstrained code is already developed and can be easily implemented to run the project in a more capable setting, such as a distributed file system. 

We have also experimented with multiple summarization techniques, including retraining existing text generators and combining algorithms to compare performance. Details of our testing process and metrics used can be found on the project report. The configuration which rendered best results for this project was the pre-trained model [BART](https://huggingface.co/facebook/bart-large-cnn).

Another consideration during the research for deployment the Pycharm project involved running an EC2 instance on AWS to deploy the database loader and maintain articles updated. By using [AWS toolkit](https://aws.amazon.com/pycharm/) extension for Pycharm, we were able to connect to a running EC2 instance, upload all the files and download the requirements to the remote machine. Although the free-tier machine could not handle the task due to RAM limitations, the project is currently deployed and ready for execution. 

## Future considerations:
There are several alternatives that we believe would improve the performance by addressing the aforementioned issues.

Most of the problems can be ameliorated by utilizing stronger computational resources, which have enough power to accelerate the execution time and handle heavy processing demands. The best alternative for this would be using distributed file systems such as Hadoop and Spark for an official deployment. 

Additionally, retraining the model with a customized dataset has the potential to improve summary qualities. This future step would require a large process of data generation and high computational power. 
