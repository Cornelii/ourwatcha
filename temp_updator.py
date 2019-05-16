import os, django
from bs4 import BeautifulSoup as BS
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final.settings')
django.setup()

from utils import Json2Json, URL_naver, Data
import requests
from movies.models import Movie
from django.db.models import Q


NAVER_ID = os.getenv('NAVER_CLOVA_ID')
NAVER_SECRET =os.getenv('NAVER_CLOVA_SECRET')
NAVER_MOVIE_BASE_URL = 'https://movie.naver.com'
MOVIE_KEY = os.getenv('MOVIE_KEY')

data = Data(**{
    'API_KEY': MOVIE_KEY,
    'NAVER_ID': NAVER_ID,
    'NAVER_SECRET': NAVER_SECRET,
    })

def large_poster_update(movie):
    name = movie.title
    try:
        openDt = movie.open_year[:4]
    except:
        openDt = None

    movie_info = data.get_naver_movie(name, openDt) # 네이버

    if movie_info:
        basic_url = movie_info[0].get('peopleUrl')
        # larget_poster_url
        lpu_res = requests.get(basic_url)
        lpu_soup = BS(lpu_res.text, 'html.parser')
        if lpu_soup.select('.poster > a > img'):
            lpu_d1 = lpu_soup.select('.poster > a > img')[0]
            lpu_d2 = lpu_d1['src']
            movie.large_poster_url = lpu_d2[:lpu_d2.find('?')] + '/'
            movie.save()

def update():
    movies = Movie.objects.filter(Q(large_poster_url__exact=None))
    print(movies)
    for movie in movies:
        large_poster_update(movie)

update()