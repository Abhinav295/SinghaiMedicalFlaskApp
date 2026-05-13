from flask import jsonify
import requests 
from bs4 import BeautifulSoup

def fetchToArticalsFromWebsit():
    """
    Fetches articles from a given website URL.
    
    :param url: The URL of the website to fetch articles from.
    :return: A list of articles fetched from the website.
    """
    
    # Placeholder for actual implementation
    articles = []
    
    url = "https://pharma.economictimes.indiatimes.com"
    response = requests.get(url)
    print("Response status code:", response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for item in soup.select(".eachStory")[:3]:
        title_tag = item.find("a")
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = url + title_tag['href']
            articles.append({
                'title': title,
                'link': link
            })
    
    return jsonify(articles)

print(fetchToArticalsFromWebsit())