import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import datetime

def scrape_cnn(max_articles_per_category):

    # datetime object containing current date and time for error log
    now = datetime.now()
    # Open error log file
    errorlog = open("../error.log", "w")

    #Start html session from requests-html library
    session = HTMLSession()

    #List of urls to query
    baseURL = 'https://www.cnn.com/'
    relativeURLs = ['World', 'Politics', 'Health', 'Entertainment', 'Business']

    # Array that will hold curated article links from all sources in the URL array
    curatedLinks = []
    topLinks = 0

    #Loop through urls
    for URL in relativeURLs:
        try:
            #Render page
            response = session.get(baseURL + URL.lower())
            response.html.render(timeout=30)

            #Find .zn containers
            containers = response.html.find('.zn')
            links = []

            # Get absolute links from zn containers
            for index, container in enumerate(containers):
                try:
                    if index > 0:
                        links.extend(container.absolute_links)
                    if index == 1:
                        topStories = len(list(dict.fromkeys(links)))
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

                if ".com/videos" in link:
                    # skip
                    print(link)
                elif "https://" in link or "http://" in link:
                    if "cnn.com/" in link:
                        if index < topStories:
                            curatedLinks.append(dict({"link": link, "top": "yes", "category": URL}))
                        else:
                            curatedLinks.append(dict({"link": link, "top": "no", "category": URL}))
                else:
                    if index < topStories:
                        curatedLinks.append(
                            dict({"link": 'https://www.cnn.com' + link, "top": "yes", "category": URL}))
                    else:
                        curatedLinks.append(
                            dict({"link": 'https://www.cnn.com' + link, "top": "no", "category": URL}))
        except:
            print("CNN - Page not found ")
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
            results = soup.find(id='body-text')

            #Dictionary to hold article info
            articleDict = dict()

            articleText = ""

            # Finding the article by class
            job_elems = results.find_all(class_='zn-body__paragraph')

            for job_elem in job_elems:
                articleText += job_elem.text

            #Add article description and url
            articleDict["description"] = articleText
            articleDict["link"] = articleURL
            articleDict["category"] = link['category']
            articleDict["source"] = "CNN"

            # Finding the headline by class
            articleDict["title"] = soup.find('h1').text

            # Check for top stories
            if link["top"] == "yes":
                articleDict["topstory"] = "Yes"
            else:
                articleDict["topstory"] = "No"

            #Finding image container
            imgContainer = soup.find(class_='l-container')

            # Finding article images
            image = imgContainer.find_all('img', class_='media__image')[0]

            if image.has_attr('data-src-medium'):
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