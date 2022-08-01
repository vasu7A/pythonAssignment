from bs4 import BeautifulSoup
import requests
import json
import re

quotes_list = []
authors_list = []
tags_list = []

pages = [
    "http://quotes.toscrape.com/",
    "http://quotes.toscrape.com/page/2/",
    "http://quotes.toscrape.com/page/3/",
    "http://quotes.toscrape.com/page/4/",
    "http://quotes.toscrape.com/page/5/",
    "http://quotes.toscrape.com/page/6/"
    "http://quotes.toscrape.com/page/7/"
    "http://quotes.toscrape.com/page/8/"
    "http://quotes.toscrape.com/page/9/"
    "http://quotes.toscrape.com/page/10/"
]


def get_author_details(next_url, author_name):
    authors_url = "http://quotes.toscrape.com/" + str(next_url['href'])
    url_response = requests.get(authors_url)
    authors_data = BeautifulSoup(url_response.text, "html.parser")
    born_date = authors_data.find("span", class_="author-born-date")
    born_place = authors_data.find(
        "span", class_="author-born-location")
    born = str(born_date.string.encode('utf-8')) + " " + \
        str(born_place.string.encode('utf-8'))
    reference = str(authors_url)+"/"
    name = author_name.string.encode('utf-8')
    authors_list.append({
        "name": name,
        "born": born,
        "reference": reference,
    })


def get_tags_list(tags):
    tags_list = []
    for each in tags:
        tags_list.append(each.string.encode('utf-8'))
    return tags_list


def get_each_quote_data(each):

    quote = each.find("span", class_="text")
    author = each.find("small", class_="author")
    tags = each.find_all("a", class_="tag")
    next_url = each.find("a", string=("(about)"))

    get_author_details(next_url, author.string)

    quotes_list.append({
        "quote": quote.string.encode("utf-8"),
        "author": author.string.encode("utf-8"),
        "tags": get_tags_list(tags)
    })


for each_url in pages:
    url = each_url
    result = requests.get(url)
    page_data = BeautifulSoup(result.text, "html.parser")
    each_quote = page_data.find_all("div", class_="quote")

    for each in each_quote:
        get_each_quote_data(each)

    data = {
        "quotes": quotes_list,
        "authors": authors_list,
    }

    with open("quotes.json", 'w') as f:
        json.dump(data, f)
        f.close()

print("Data Transfer Completed!")
