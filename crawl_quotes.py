from bs4 import BeautifulSoup
import requests
import json
import re


def get_author_details(author_details_url, author_name, authors_list,
                       unique_authors_supporting_list):

    authors_url = "http://quotes.toscrape.com" + \
        str(author_details_url['href'])
    url_response = requests.get(authors_url)
    authors_data = BeautifulSoup(url_response.text, "html.parser")
    born_date = authors_data.find("span", class_="author-born-date")
    born_place = authors_data.find(
        "span", class_="author-born-location")
    born = str(born_date.string.encode('utf-8')) + " " + \
        str(born_place.string.encode('utf-8'))
    reference = str(authors_url)+"/"
    name = author_name
    if(name not in unique_authors_supporting_list):
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


def get_quote_div_data(each_div,  authors_list, quotes_list,
                       unique_authors_supporting_list):
    quote = each_div.find("span", class_="text")
    author = each_div.find("small", class_="author")
    tags = each_div.find_all("a", class_="tag")
    author_details_url = each_div.find("a", string=("(about)"))
    author = str(author.string.encode("utf-8"))
    encoded_quote = quote.text.encode('utf-8')
    quote_formatted = re.sub("[^\w\s.,']", '', encoded_quote)
    if('\xc3' in author):
        author = "Andre Gide"
    get_author_details(author_details_url, author,
                       authors_list, unique_authors_supporting_list)
    if(author not in unique_authors_supporting_list):
        quotes_list.append({
            "quote": quote_formatted,
            "author": author,
            "tags": get_tags_list(tags)
        })

    unique_authors_supporting_list.append(author)


def main():
    quotes_list = []
    authors_list = []
    unique_authors_supporting_list = []
    tags_list = []

    url = "http://quotes.toscrape.com/"
    while True:
        print(url)
        result = requests.get(url)
        page_data = BeautifulSoup(result.text, "html.parser")
        each_quote_div = page_data.find_all("div", class_="quote")

        for each_div in each_quote_div:
            get_quote_div_data(each_div, authors_list,
                               quotes_list, unique_authors_supporting_list)

        is_next_page_exists = page_data.select_one('li.next>a')
        next_page_tag = page_data.find('li', "next")
        if(is_next_page_exists != None):
            base_url = "http://quotes.toscrape.com"
            next_page_url = is_next_page_exists['href']
            url = base_url+str(next_page_url)
        else:
            break

    data = {
        "quotes": quotes_list,
        "authors": authors_list,
    }

    with open("quotes.json", 'w') as f:
        json.dump(data, f)

    print("Data Transfer Completed!")


main()
