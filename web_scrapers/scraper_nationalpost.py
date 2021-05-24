import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import datetime
import time

def scrape_nationalpost(max_articles_per_category):

    # datetime object containing current date and time for error log
    now = datetime.now()
    # Open error log file
    errorlog = open("../error.log", "w")

    #Start html session from requests-html library
    session = HTMLSession()

    #List of urls to query
    baseURL = 'https://nationalpost.com/category/news/'
    relativeURLs = ['Canada']

    # Array that will hold curated article links from all sources in the URL array
    curatedLinks = []
    topLinks = 0

    #Loop through urls
    for URL in relativeURLs:
        try:
            # Render page
            response = session.get(baseURL)
            response.html.render(timeout=20)

            # Find .zn containers
            containerTop = response.html.find('.hero-feed')
            containerRest = response.html.find('.feed-section')
            links = []

            # Get absolute links from zn containers
            for index, container in enumerate(containerTop):
                try:
                    links.extend(container.absolute_links)
                    topStories = len(list(dict.fromkeys(links)))
                except:
                    errorlog.write(now.strftime("%m/%d/%Y, %H:%M:%S") + " - Failed to open container." + "\n")
            # Get absolute links from zn containers
            for index, container in enumerate(containerRest):
                try:
                    links.extend(container.absolute_links)
                except:
                    errorlog.write(now.strftime("%m/%d/%Y, %H:%M:%S") + " - Failed to open container." + "\n")

            #Removing duplicates
            links = list(dict.fromkeys(links))

            # Add top links by category
            topLinks+= max_articles_per_category

            # Loop through those links and add absolute path, when it is not contained
            for index, link in enumerate(links):
                # Keep top curated links
                if len(curatedLinks) >= topLinks:
                    break

                if ".com/videos" in link:
                    # skip
                    print(link)
                elif "https://" in link or "http://" in link:
                    if "nationalpost.com" in link:
                        if index < topStories:
                            curatedLinks.append(dict({"link": link, "top": "yes", "category": URL}))
                        else:
                            curatedLinks.append(dict({"link": link, "top": "no", "category": URL}))
                else:
                    if index < topStories:
                        curatedLinks.append(
                            dict({"link": 'https://nationalpost.com/category/news/' + link, "top": "yes", "category": URL}))
                    else:
                        curatedLinks.append(
                            dict({"link": 'https://nationalpost.com/category/news/' + link, "top": "no", "category": URL}))
        except:
            print("Page not found ")
            errorlog.write(now.strftime("%m/%d/%Y, %H:%M:%S") + " - Failed to open " + URL + "\n")

    #Articles array
    articles = []
    notFound = 0
    imgNotFound = 0

    #Loop through curated links
    for link in curatedLinks:
        print(link, end='\n')
        try:
            #Use beautiful soup to access the link
            articleURL = link['link']
            page = requests.get(articleURL)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Find text container in the link
            results = soup.find_all(class_='article-content__content-group')

            #Dictionary to hold article info
            articleDict = dict()

            articleText = ""

            for result in results:
                try:
                    # Finding the article by class
                    job_elems = result.find_all('p')

                    for job_elem in job_elems:
                        articleText += job_elem.text
                except:
                    print("No paragraph here")

            #Add article description and url
            articleDict["description"] = articleText
            articleDict["link"] = articleURL
            articleDict["category"] = link['category']
            articleDict["source"] = "NationalPost"

            # Finding the headline by class
            articleDict["title"] = soup.find('h1').text

            # Check for top stories
            if link["top"] == "yes":
                articleDict["topstory"] = "Yes"
            else:
                articleDict["topstory"] = "No"

            # Finding article images
            image = soup.find_all(class_='featured-image__image')[0]

            if image.has_attr('data-src'):
                articleDict["img"] = image['data-src']
            elif image.has_attr('src'):
                articleDict["img"] = "https:" + image['src']
            elif image.has_attr('data-src-medium'):
                articleDict["img"] = "https:" + image['data-src-medium']
            elif image.has_attr('data-src-small'):
                articleDict["img"] = "https:" + image['data-src-small']

            #Append article to article dictionary
            articles.append(articleDict)

        except AttributeError:
            notFound += 1
            errorlog.write(now.strftime("%m/%d/%Y, %H:%M:%S") + " - Attribute Error\n")
        except IndexError:
            imgNotFound += 1
            errorlog.write(now.strftime("%m/%d/%Y, %H:%M:%S") + " - Image not found\n")
            # Append article to article dictionary
            try:
                if articleDict['description'] != "":
                    articles.append(articleDict)
            except:
                print("No dict to append")


    errorlog.close()

    return articles