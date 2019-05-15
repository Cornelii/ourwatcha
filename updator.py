import os, django
from bs4 import BeautifulSoup as BS
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final.settings')
django.setup()

from utils import *
from utils import Data

# importing models
from movies.models import Movie, Genre, Trailer
from people.models import People, Role

NAVER_ID = os.getenv('NAVER_CLOVA_ID')
NAVER_SECRET =os.getenv('NAVER_CLOVA_SECRET')
MOVIE_KEY = os.getenv('MOVIE_KEY')
NAVER_MOVIE_BASE_URL = 'https://movie.naver.com'

BOXOFFICE_FLAG = True

data = Data(**{
    'API_KEY': MOVIE_KEY,
    'NAVER_ID': NAVER_ID,
    'NAVER_SECRET': NAVER_SECRET,
    })

## get movie_list
movie_list_query = {
    'itemPerPage': 100,
    'openStartDt': 2019,
    'openEndDt': 2020,
    #'flag':'',
    # 'flag'
}

## weekly boxoffcie query
weekly_boxoffice_query = {
    'weekGb':0,
}


## 영화정보에서 네이버를 통해서 정보 얻어오기.
def actor_update(movie):
    name = movie.title
    try:
        openDt = movie.open_year[:4]
    except:
        openDt = None

    # naver search api
    movie_info = data.get_naver_movie(name, openDt) # 네이버

    if movie_info:
        # poster_url update
        movie.poster_url = movie_info[0].get('poster_url')

        actor_names = movie_info[0].get('actors').split('|')
        director_names = movie_info[0].get('directors').split('|')
        people_names = actor_names + director_names

        # naver에서 배우 imag들 스크랩핑
        basic_url = movie_info[0].get('peopleUrl')
        detail_url = basic_url.replace('basic','detail')
        res = requests.get(detail_url+'#tab/')
        # peopleUrl is not correct
        soup = BS(res.text, 'html.parser')
        img_tags = soup.select('.p_thumb > a > img')
        actor_imgs = {}
        for tag in img_tags:
            actor_imgs.update({tag['alt']: tag['src']})

        # naver에서 배우 배역 스크랩핑
        role_tags = soup.select('div.p_info')
        actor_roles = {}
        for tag in role_tags:
            key = tag.select_one('a.k_name')['title']
            value1 = tag.select_one('em.p_part').string
            value2 = tag.select_one('span').string
            actor_roles.update({key: [value1, value2]})

        for name in people_names:
            if name:
                actor_list_query = {
                    'peopleNm': name
                }
                # TODO: 동명이의인 처리
                actor_info = data.get_actor_list(5, **actor_list_query)
                for target_actor in actor_info:
                    if movie.title in target_actor.get('filmography').split('|'):
                        actor_info[0] = target_actor
                        break

                if actor_info:
                    role = actor_info[0].pop('role')
                    # role instance 생성
                    try:
                        role_obj = Role.objects.get(type_name=role)
                    except:
                        role_obj = Role.objects.create(**{'type_name':role})
                    try:
                        person = People.objects.get(code=actor_info[0].get('code'))
                    except:
                        person = People.objects.create(**actor_info[0])
                        movie.people.add(person)
                        person.portrait_url = actor_imgs.get(name)
                    person.roles.add(role_obj)
                    person.save()
        # description
        res_des = requests.get(movie_info[0].get('peopleUrl'))
        soup_des = BS(res_des.text, 'html.parser')
        if soup_des.select('p.con_tx'):
            text_des = soup_des.select('p.con_tx')[0].text
            description = text_des.replace('\r\xa0', '')
            movie.description = description
        movie.save()
        # trailer_url
        res_v1 = requests.get(movie_info[0].get('peopleUrl'))
        soup_v1 = BS(res_v1.text, 'html.parser')
        if soup_v1.select('ul.video_thumb > li > a'):
            url_v = soup_v1.select('ul.video_thumb > li > a')[0]['href']

            res_v2 = requests.get(NAVER_MOVIE_BASE_URL + url_v)
            soup_v2 = BS(res_v2.text, 'html.parser')
            iframes = soup_v2.select('div.video_ar > iframe')
            for frame in iframes:
                trail_clip = frame['src']
                Trailer.objects.create(trailer_url=NAVER_MOVIE_BASE_URL+trail_clip, movie=movie)


if BOXOFFICE_FLAG:
    movie_list = data.get_movie_list_from_boxoffice(104, '20181224', **weekly_boxoffice_query)
else:
    movie_list = data.get_movie_list(5, **movie_list_query)
print(movie_list)
for movie in movie_list:
    try:
        # sales and audience update case when using weekly boxoffice
        existing_movie = Movie.objects.get(id=movie.get('id'))
        print("Unique Constraint failed with {}".format(movie.get('title')))
        if existing_movie.sales and movie.get('sales'):
            if existing_movie.sales < int(movie.get('sales')):
                existing_movie.sales = int(movie.get('sales'))
                existing_movie.save()
        elif movie.get('sales'):
            existing_movie.sales = int(movie.get('sales'))
            existing_movie.save()
        if existing_movie.audience and movie.get('audience'):
            if existing_movie.audience < int(movie.get('audience')):
                existing_movie.audience = int(movie.get('audience'))
                existing_movie.save()
        elif movie.get('audience'):
            existing_movie.audience = int(movie.get('audience'))
            existing_movie.save()
    except:
        if data.get_movie_detail(movieCd=movie.get('id')):
            movie_detail = data.get_movie_detail(movieCd=movie.get('id'))[0]
            genre_flag = True
            nation_flag = True
            try:
                genre = movie_detail.pop('genre')
            except:
                genre_flag = False
            try:
                nation = movie_detail.pop('nation')
            except:
                nation_flag = False
            try:
                movie_detail['running_time'] = int(movie_detail.get('running_time'))
            except:
                movie_detail['running_time'] = -1
            # nation 처리

            if nation_flag:
                tmp_nation = []
                for nat in nation:
                    tmp_nation.append(nat.get('nationNm'))

                movie_detail.update(nation="|".join(tmp_nation))
            movie.update(movie_detail)
            obj = Movie.objects.create(**movie)
            # genre 처리
            if genre_flag:
                for gen in genre:
                    try:
                        genre_obj = Genre.objects.create(type_name=gen.get('genreNm'))
                    except:
                        genre_obj = Genre.objects.get(type_name=gen.get('genreNm'))
                    obj.genre.add(genre_obj)
            actor_update(obj)






## TODO: 영화배우 초기 스크래핑
def actor_append(movie):
    pass

## TODO: 업데이트가 필요한 데이터 업데이터 만들기.



