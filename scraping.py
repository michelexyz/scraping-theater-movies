import requests
from bs4 import BeautifulSoup
import time

from datetime import date

import tmdbsimple as tmdb
tmdb.API_KEY = '5910249ad580ba9580015e70986600d5'

tmdb.REQUESTS_TIMEOUT = (2, 5) 

tmdb.REQUESTS_SESSION = requests.Session()

# genre list

genres = tmdb.Genres().movie_list()['genres']

genre_dict = {}


for genre in genres:
    genre_dict[genre['id']] = genre['name']

print(genre_dict)


search = tmdb.Search()

today = date.today()


# Step 1: Scrape the Movie Program List
def get_movies_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Finding all movie titles within the table with class "agenda"
    movies = soup.find_all('table', class_='agenda')
    
    movie_titles = []
    for table in movies:
        # Finding all anchor tags within the table
        links = table.find_all('a')
        for link in links:
            title = link.text.strip()
            if title:
                movie_titles.append(title)
                
    return movie_titles

def get_movies_by_day(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Dictionary to store movies per day
    movies_by_day = {}

    agenda = soup.find('table', class_='agenda')

    rows = agenda.find_all('tr', class_=lambda x: x and x.startswith('day'))

    # Find all rows of the table
    rows = soup.find_all('tr', class_=lambda x: x and x.startswith('day'))

    for row in rows:
        # Extract the day class (e.g., 'day0', 'day1', ...)
        day_class = row.get('class')[0]

        # Initialize the day key if not already in the dictionary
        if day_class not in movies_by_day:
            movies_by_day[day_class] = []

        # Find all <td> elements
        td_elements = row.find_all('td')
        if len(td_elements) >= 3:
            # Movie time is in the first <td>
            time_tag = td_elements[0].find('a')
            movie_time = time_tag.text.strip() if time_tag else "N/A"

            # Movie title is in the second <td>
            title_tag = td_elements[1].find('a')
            movie_title = title_tag.text.strip() if title_tag else "N/A"

            # Theather name is in the third <td>
            theater_tag = td_elements[2].find('span')
            theater_name = theater_tag.text.strip() if theater_tag else "N/A"


            # Add movie details to the list for the day
            movie_details = {
                'title': movie_title,
                'time': movie_time,
                'theater': theater_name,
            }
            movies_by_day[day_class].append(movie_details)
              

    return movies_by_day

# function to get the id of each unique movie, release date, genre and letterboxd rating

def get_movie_tmdb_info(movie_title):
    search = tmdb.Search()
    response = search.movie(query=movie_title)
    movie_id = search.results[0]['id']
    movie_release_date = search.results[0]['release_date']
    movie_genre = search.results[0]['genre_ids']

    # get the genre names
    genre_names = []

    for genre in movie_genre:
        genre_names.append(genre_dict[genre])


    return movie_id, movie_release_date, genre_names

# Step 2: Get the Letterboxd rating

#def get_letterboxd_rating(movie_id):
     


# def get_letterboxd_rating(movie_title):
#     search_url = f"https://letterboxd.com/search/{movie_title.replace(' ', '%20')}/"
#     response = requests.get(search_url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Extract the rating from the search results page
#     rating_tag = soup.find('span', class_='rating')
    
#     if rating_tag:
#         rating = rating_tag.text.strip()
#     else:
#         rating = "N/A"
    
#     return rating

# TODO rewrite the function
def print_movie_ratings(movie_titles):
    for title in movie_titles:
        rating = get_letterboxd_rating(title)
        print(f"{title}: {rating}")
        time.sleep(1)  # To avoid hitting the server too quickly and getting blocked

# Replace this URL with the actual URL of the movie program list
movie_program_url = 'https://www.lab111.nl/agenda/listview'  # Example URL, replace with actual
movies_list = get_movies_by_day(movie_program_url)
print(movies_list)
