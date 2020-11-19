#!pip install beautifulsoup4
#!pip install lxml
import requests
import json
from bs4 import BeautifulSoup
all_articles = []
def parse_page(url):
  raw_data_list = []
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  dates = [_.get_text()[1:11] for _ in soup.find_all('div', class_='penci-box-meta')]
  articles = soup.find_all('h2')

  for i, a in enumerate(articles[1:]):
    cur_article = {}
    a = a.find('a')
    cur_article['title'] = a.get_text()
    cur_article['date'] = dates[i]
    cur_article['url'] = a['href']
    pg = requests.get(a['href'])
    sp = BeautifulSoup(pg.content, 'html.parser')
    cur_article['raw_text'] = [_.get_text().replace("\xa0", " ") for _ in sp.find_all('p')][:-14]
    raw_data_list.append(cur_article)
  return raw_data_list

all_articles += parse_page('http://keskil14.ru/category/detyam/sahalyy-detyam/')
for i in range(2,13):
  all_articles += parse_page('http://keskil14.ru/category/detyam/sahalyy-detyam/page/'+str(i))
all_articles += parse_page('http://keskil14.ru/category/detyam/sahalyy/')
for i in range(2,17):
  all_articles += parse_page('http://keskil14.ru/category/detyam/sahalyy/page/'+str(i))

with open('raw_data_keskil.json', 'w') as outfile:
    json.dump(all_articles, outfile, ensure_ascii=False)
