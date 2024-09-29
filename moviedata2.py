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

    output_file = 'movie_data2.csv'
    
    # Open the CSV file for writing
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Directors', 'Writers', 'Stars', 'Genre'])  # Write header row

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

            # # Check for directors, writers, stars, and genres
            container_list = movie_soup.find_all("div", class_="ipc-metadata-list-item__content-container")
            director_cont = container_list[0]
            directors = director_cont.find("ul").find_all("li")
            directors_text = [entry.find('a') for entry in directors]
            directors_text = [entry.text.strip() for entry in directors_text]
            director = ', '.join(directors_text)
        
            screenwriter_cont = container_list[1]
            screenwriters = screenwriter_cont.find("ul").find_all("li")
            screenwriters_text = [entry.find('a') for entry in screenwriters]
            screenwriters_text = [entry.text.strip() for entry in screenwriters_text]
            screenwriter = ', '.join(screenwriters_text)

            stars_cont = container_list[2]
            stars = stars_cont.find("ul").find_all("li")
            stars_text = [entry.find('a') for entry in stars]
            stars_text = [entry.text.strip() for entry in stars_text]
            star = ', '.join(stars_text)

            # Check for genres
            genrelist = movie_soup.find("div", class_="ipc-chip-list__scroller")
            genres = genrelist.find_all("a")
            genres_text = [anchor.find("span") for anchor in genres]
            genres_text = [entry.text.strip() for entry in genres_text if entry]
            genre = ', '.join(genres_text) if genres_text else 'N/A'

            # Write the movie data to the CSV
            writer.writerow([title, director, screenwriter, star, genre])
except Exception as e:
    print(e)
