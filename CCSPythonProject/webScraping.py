import requests
from bs4 import BeautifulSoup
import pandas as pd
# import sys

# review_dict = {'Name': [], 'Date': [], 'Review': []}
review_dict = {'Review': []}
# page_amount = 1

url = 'https://www.metacritic.com/movie/avatar-the-way-of-water'
# url = sys.argv
url += '/user-reviews'
user_agent = {'User-agent': 'Chrome/39.0.2171.95'}
response = requests.get(url, headers=user_agent)

soup = BeautifulSoup(response.text, 'html.parser')

for review in soup.find_all('div', class_='pages'):
    if review.find('li', class_='page last_page').find('a').text:
        page_amount = int(review.find('li', class_='page last_page').find('a').text)
    else:
        page_amount = 1

for page in range(0, page_amount):

    url2 = url + '?page=' + str(page)
    user_agent = {'User-agent': 'Chrome/39.0.2171.95'}
    response = requests.get(url2, headers=user_agent)

    soup = BeautifulSoup(response.text, 'html.parser')

    for review in soup.find_all('div', class_='review pad_top1'):
        # review_dict['Name'].append(review.find('span', class_='author').find('a').text)
        # review_dict['Date'].append(review.find('span', class_='date').text)
        if review.find('span', class_='blurb blurb_expanded'):
            review_dict['Review'].append(review.find('span', class_='blurb blurb_expanded').text)
        else:
            review_dict['Review'].append(review.find('div', class_='review_body').find('span').text)

reviews = pd.DataFrame(review_dict)
reviews.to_csv('results.csv', index=False, encoding='utf-8')