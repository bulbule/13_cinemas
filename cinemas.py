import argparse

from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException


AFISHA_URL = 'https://www.afisha.ru/msk/schedule_cinema/'
KINOPOISK_URL = 'https://www.kinopoisk.ru/index.php'
NUM_MOVIES = 10
HEADERS = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12 AppleWebKit/602.4.8'
    '(KHTML, like Gecko) Version/10.0.3 Safari/602.4.8'
     }


def fetch_afisha_page():
    response = requests.get(AFISHA_URL).content
    return BeautifulSoup(response, 'html.parser')


def get_movie_title(movie_tag):
    return movie_tag.find('h3', class_='usetags').find('a').get_text()


def get_movies_tags(afisha):
    return afisha.find(class_='b-theme-schedule m-schedule-with-collapse').\
        find_all(class_='object s-votes-hover-area collapsed')


def get_cinemas_for_movie(movie_tag):
    cinemas = []
    cinemas_tags = movie_tag.find_all('td', class_='b-td-item')
    for cinema_tag in cinemas_tags:
        cinemas.append(cinema_tag.find('a').get_text())
    return cinemas


def get_movie_rating_and_votes(movie_title):
    payload = {
        'first': 'yes',
        'kp_query': movie_title
    }
    try:
        movie_request = requests.get(KINOPOISK_URL,
                                     headers=HEADERS,
                                     params=payload,
                                     timeout=5
                                     )
    except RequestException:
        return 0, 0
    movie_soup = BeautifulSoup(movie_request.content, 'html.parser')
    rating = movie_soup.find('span', class_='rating_ball')
    votes = movie_soup.find('span', class_='ratingCount')
    rating = float(rating.get_text()) if rating is not None else 0
    votes = int(
        votes.get_text().replace(
            '\xa0',
            '')) if votes is not None else 0
    return rating, votes


def collect_movies_info(afisha):
    movies_info = []
    for movie_tag in get_movies_tags(afisha):
        movie_title = get_movie_title(movie_tag)
        movies_info.append({'movie': movie_title,
                            'cinemas': len(get_cinemas_for_movie(movie_tag)),
                            'rating': get_movie_rating_and_votes(movie_title)[0],
                            'votes': get_movie_rating_and_votes(movie_title)[1]
                            })
    return movies_info


def sort_movies_by_rating(movies_info):
    return sorted(movies_info, key=lambda movie: movie['rating'], reverse=True)


def sort_movies_by_cinemas(movies_info):
    return sorted(
        movies_info,
        key=lambda movie: movie['cinemas'],
        reverse=True)


def output_movies(movies_info):
    for movie in movies_info[:NUM_MOVIES]:
        print(
            '{}, rating:{}, votes:{}, cinemas:{}'.format(
                movie['movie'],
                movie['rating'],
                movie['votes'],
                movie['cinemas']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cinemas', action='store_true',
                        help='switch to sorting by cinemas')
    args = parser.parse_args()
    afisha = fetch_afisha_page()
    movies_info = collect_movies_info(afisha)
    if args.cinemas:
        movies_info = sort_movies_by_cinemas(movies_info)
    else:
        movies_info = sort_movies_by_rating(movies_info)
    output_movies(movies_info)
