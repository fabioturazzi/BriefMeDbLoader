import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import datetime
import time

def scrape_cbc(max_articles_per_category):

    # datetime object containing current date and time for error log
    now = datetime.now()
    # Open error log file
    errorlog = open("error.log", "w")

    #List of urls to query
    baseURL = 'https://www.cbc.ca/news/'
    relativeURLs = ['local', 'thenational', 'canada', 'politics', 'indigenous']

    # Array that will hold curated article links from all sources in the URL array
    curatedLinks = []
    topLinks = 0

    #Loop through urls
    for URL in relativeURLs:
        try:
            agent = {"User-Agent": "Mozilla/5.0"}
            #Render page
            page = requests.get(baseURL + URL.lower(), headers=agent)
            time.sleep(0.1)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Find text container in the link
            containers = soup.find(class_='pageComponent')
            links = []
            #Get absolute links from zn containers
            for container in containers:
                try:
                    links.extend(container.find_all('a'))
                except:
                    errorlog.write(now.strftime("%m/%d/%Y, %H:%M:%S") + " - Failed to open container." + "\n")

            #Removing duplicates
            links = list(dict.fromkeys(links))

            # Add top links by category
            topLinks+= max_articles_per_category

            #Loop through those links and add absolute path, when it is not contained
            for index, link in enumerate(links):
                # Keep top curated links
                if len(curatedLinks) >= topLinks:
                    break

                if link.has_attr('href') and len(link['href'].replace(baseURL, "")) > 30:
                    if "player/play" in link['href']:
                        # skip
                        print(link['href'])
                    elif "https://" in link['href'] or "http://" in link['href']:
                        if "cbc.ca/" in link['href']:
                            if index < 10:
                                curatedLinks.append(dict({"link": link['href'], "top": "yes", "category": URL}))
                            else:
                                curatedLinks.append(dict({"link": link['href'], "top": "no", "category": URL}))
                    else:
                        if index < 10:
                            curatedLinks.append(
                                dict({"link": 'https://www.cbc.ca' + link['href'], "top": "yes", "category": URL}))
                        else:
                            curatedLinks.append(
                                dict({"link": 'https://www.cbc.ca' + link['href'], "top": "no", "category": URL}))
        except:
            print("Page not found")
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
            results = soup.find(class_='storyWrapper')

            #Dictionary to hold article info
            articleDict = dict()

            articleText = ""

            # Finding the article by class
            job_elems = results.find_all('p')

            for job_elem in job_elems:
                articleText += job_elem.text

            #Add article description and url
            articleDict["description"] = articleText
            articleDict["link"] = articleURL
            articleDict["category"] = "Canada"
            articleDict["source"] = "CBC"

            # Finding the headline by class
            articleDict["title"] = soup.find('h1').text

            # Check for top stories
            if link["top"] == "yes":
                articleDict["topstory"] = "Yes"
            else:
                articleDict["topstory"] = "No"

            imgContainer = soup.find(class_="leadmedia-story")

            if imgContainer is not None:
                # Finding article images
                image = imgContainer.find_all('img')[0]

                if image.has_attr('src'):
                    articleDict["img"] = image['src']
                elif image.has_attr('data-src-medium'):
                    articleDict["img"] = "https:" + image['data-src-medium']
                elif image.has_attr('data-src'):
                    articleDict["img"] = "https:" + image['data-src']
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
                articles.append(articleDict)
            except:
                print("No dict to append")


    errorlog.close()

    return articles