import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import csv

try:
    url = 'https://www.imdb.com/chart/top/'

    driver = webdriver.Chrome()
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    movies = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 dHaCOW compact-list-view ipc-metadata-list--base").find_all('li')

    with open('movies.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Title', 'Year', 'Rating'])

        for movie in movies:
            fullname = movie.find('a', class_='ipc-title-link-wrapper').find('h3').text.strip()
            rank, title = fullname.split('.', 1)
            rank = rank.strip()
            title = title.strip()
            year = movie.find('span', class_='sc-b189961a-8 hCbzGp cli-title-metadata-item').text
            rating = movie.find('span', class_="ipc-rating-star--rating").text
            writer.writerow([rank, title, year, rating])

except Exception as e:
    print(e)
