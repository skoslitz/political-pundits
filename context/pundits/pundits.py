import json
import requests
import bs4
from newspaper import Article

def retrieve_snippets(query):
    '''
    takes in a query (keyword) and returns a list of relevant snippets if that keyword exists, else returns false
    snippets are dictionaries with the following keys:
        name: name of pundit
        title: the pundit's credentials
        keyword: query keyword
        source: where the text came from (twitter or cfr)
        url: url to the full text (article or tweet)
        text: body of the snippet
    '''

    snippets = []

    with open('panel/panel.json', "r") as json_file:
        panel = json.loads(json_file.read())
        if query in panel.keys():
            for user in panel[query]:
                for link in user['links']:
                    if user['links'][link]:
                        snippet = {}
                        snippet['name'] = user['name']
                        snippet['title'] = user['title']
                        snippet['keyword'] = query
                        url = user['links'][link]
                        snippets = build_snippets(query, link, url, snippet)
        else:
            return False

    return snippets


def build_snippets(query, website, url, snippet):
    '''
    takes in the query, website, url, and snippet, and constructs the full snippet
    '''
    snippets = []
    snippet['source'] = website
    if website == "cfr":
        response = requests.get(url + "#publications")
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        for article in soup.select('article.publication_spotlight h3 a'):
            href = str(article.attrs.get('href'))
            full_url = "http://www.cfr.org/" + href
            article = Article(full_url)
            article.download()
            article.parse()
            article.nlp()
            if query in article.keywords:
                snippet['text'] = article.summary
                snippet['url'] = full_url
                snippets.append(snippet)
    elif website == "twitter":
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        for tweet in soup.select('div.tweet'):
            if tweet.select('div.content p.tweet-text'):
                tweet_content = tweet.select('div.content p.tweet-text')[0].text
                if tweet.select('small.time a'):
                    tweet_url = tweet.select('small.time a')[0].attrs.get('href')
                    tweet_content_lower = tweet_content.lower()
                    if query in tweet_content:
                        snippet['text'] = tweet_content
                        snippet['url'] = "http://twitter.com" + tweet_url
                        snippets.append(snippet)

    return snippets
