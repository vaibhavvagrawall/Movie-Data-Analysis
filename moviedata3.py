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

    output_file = 'movie_data3.csv'
    
    # Open the CSV file for writing
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Country', 'Language'])

        for movie in movies:
            fullname = movie.find('a', class_='ipc-title-link-wrapper').find('h3').text.strip()
            rank, title = fullname.split('.', 1)
            title = title.strip()

            movie_url = 'https://www.imdb.com' + movie.find('a', class_='ipc-title-link-wrapper')['href']
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            movie_response = requests.get(movie_url, headers=headers)
            movie_soup = BeautifulSoup(movie_response.content, 'html.parser')

            # Locate the container for title details
            details_section = movie_soup.find("div",class_ ="sc-f65f65be-0 dQVJPm", attrs={'data-testid': 'title-details-section'})
        
            # Extract country data
            countries_cont = details_section.find('li', class_="ipc-metadata-list__item", attrs={'data-testid': 'title-details-origin'}) 
            countries = countries_cont.find_all("li", class_="ipc-inline-list__item")
            countries_text = [entry.find('a').text.strip() for entry in countries]
            country = ', '.join(countries_text)
            
            # Extract language data
            languages_cont = details_section.find('li', class_="ipc-metadata-list__item", attrs={'data-testid': 'title-details-languages'})
            languages = languages_cont.find_all("li",class_="ipc-inline-list__item")
            languages_text = [entry.find('a').text.strip() for entry in languages]
            language = ', '.join(languages_text)

            writer.writerow([title, country, language])
except Exception as e:
    print(f"Error: {e}")
