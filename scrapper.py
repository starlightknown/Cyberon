import requests 
from bs4 import BeautifulSoup

def scrape(URL):
    res = requests.get(URL) 
    soup = BeautifulSoup(res.text, 'html.parser')
    item = soup.find('div', class_="BNeawe s3v9rd AP7Wnd")
    i = soup.find('span', class_="BNeawe")
    link = i.find('a')
    print(link)
    return(item, link['href'])

def advscrape(URL): 
    res = requests.get(URL) 
    soup = BeautifulSoup(res.text, 'html.parser')
    for item in soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi"):
        return(item)