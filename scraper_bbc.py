import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import datetime
import time

def scrape_bbc(max_articles_per_category):

    # datetime object containing current date and time for error log
    now = datetime.now()
    # Open error log file
    errorlog = open("error.log", "w")

    #Start html session from requests-html library
    session = HTMLSession()

    #List of urls to query
    baseURL = 'https://www.bbc.com/news/'
    relativeURLs = ['Coronavirus', 'World', 'Business', 'Tech', 'Science', 'Entertainment_and_Arts', 'Health']

    # Array that will hold curated article links from all sources in the URL array
    curatedLinks = []
    topLinks = 0

    #Loop through urls
    for URL in relativeURLs:
        print(baseURL + URL.lower())
        try:
            agent = {"User-Agent": "Mozilla/5.0"}
            #Render page
            page = requests.get(baseURL + URL.lower(), headers=agent)
            time.sleep(0.1)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Find text container in the link
            containers = soup.find_all(id='index-page')

            topContainer = soup.find(id='topos-component')
            if topContainer is not None:
                stories = topContainer.find_all('a')
                topStories = len(list(dict.fromkeys(stories)))
            else:
                topStories = 10

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
            for index,link in enumerate(links):
                # Keep top curated links
                if len(curatedLinks) >= topLinks:
                    break

                if link.has_attr('href') and any(char.isdigit() for char in link['href']):
                    if "player/play" in link['href']:
                        # skip
                        print(link['href'])
                    elif "https://" in link['href'] or "http://" in link['href']:
                        if index < topStories:
                            curatedLinks.append(dict({"link": link['href'], "top": "yes", "category": URL}))
                        else:
                            curatedLinks.append(dict({"link": link['href'], "top": "no", "category": URL}))
                    else:
                        if index < topStories:
                            curatedLinks.append(dict({"link": 'https://www.bbc.com' + link['href'], "top": "yes", "category": URL}))
                        else:
                            curatedLinks.append(dict({"link": 'https://www.bbc.com' + link['href'], "top": "no", "category": URL}))
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
            results = soup.find(class_='ssrcss-5h7eao-ArticleWrapper')

            #Dictionary to hold article info
            articleDict = dict()

            articleText = ""

            # Finding the article by class
            job_elems = results.find_all('div')

            for job_elem in job_elems:
                if job_elem.has_attr('data-component') and job_elem['data-component'] == 'text-block':
                    articleText += job_elem.text

            #Add article description and url
            articleDict["description"] = articleText
            articleDict["link"] = articleURL
            categories = {'Coronavirus': 'Health', 'World':'World', 'Business':'Business',
                          'Tech': 'Technology', 'Science': 'Science', 'Entertainment_and_Arts': 'Entertainment', 'Health': 'Health'}
            articleDict["category"] = categories[link['category']]
            articleDict["source"] = "BBC"

            # Finding the headline by class
            articleDict["title"] = soup.find('h1').text

            # Check for top stories
            if link["top"] == "yes":
                articleDict["topstory"] = "Yes"
            else:
                articleDict["topstory"] = "No"

            # Finding article images
            image = results.find('div', recursive=False).find_all('img')[0]

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