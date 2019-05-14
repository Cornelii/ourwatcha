import json
import requests
from datetime import datetime, timedelta

TIMEDELTA_A_WEEK = timedelta(days=-7)

class Json2Json:
    def __init__(self):
        self.map = None
        self.keys = None
        self.values = None
        self.transfered = []

    def set_map(self, _map):
        '''
        map is a dictionary key: from_json value, value: to_json value
        :param map:
        :return:
        '''
        self.map = _map
        self.keys = list(_map.keys())
        self.values = set(_map.values())

    def json2json_list(self, url, **kwargs):  # kwargs => method, data, headers
        result = []
        method = kwargs.pop('method')
        try:
            if method == 'GET':
                res = requests.get(url, **kwargs)
            elif method == 'POST':
                res = requests.post(url, **kwargs)
        except:
            raise "error ! {}".format(res.status_code)
        parsed_res = res.json()
        result = self.find_values(parsed_res)
        return result

    def dfs(self, obj, tmp_dict):
        if type(obj) == dict:
            for key, val in obj.items():
                if key in self.keys:
                    if self.map[key] in tmp_dict.keys():
                        self.transfered.append(tmp_dict)
                        tmp_dict = {}
                    tmp_dict.update({self.map[key]: val})
                else:
                    if type(val) == dict:
                        tmp_dict = self.dfs(val, tmp_dict)
                    elif type(val) == list:
                        for sub_val in val:
                            tmp_dict = self.dfs(sub_val, tmp_dict)
        elif type(obj) == list:
            for sub_obj in obj:
                tmp_dict = self.dfs(sub_obj, tmp_dict)
        return tmp_dict

    def find_values(self, parsed_res):
        self.transfered = []
        tmp_dict = self.dfs(parsed_res, tmp_dict={})
        if tmp_dict:
            self.transfered.append(tmp_dict)
        return self.transfered

movie_list_json_relations = {
    'movieCd':'id',
    'movieNm':'title',
    'movieNmEn':'en_title',
    'openDt':'open_year',
    'prdtYear':'prdt_year',
}

movie_detail_json_relations = {
    'genres': 'genre',
    'showTm': 'running_time',
    'watchGradeNm': 'grade',
    'nations': 'nation',
    'prdtStatNm': 'state',
    'movieNmEn': 'en_title',
    'prdtYear': 'prdt_year'
}

actor_list_json_relations = {
    'peopleCd': 'code',
    'peopleNm':'name',
    'peopleNmEn':'en_name',
    'repRoleNm':'role', # 감독, 배우, or others 시나리오 각본 등.
    'filmoNames':'filmography',
}

actor_detail_json_relations = {
    'movieCd':'movies',
}

naver_json_relations = {
    'link': 'peopleUrl',
    'image': 'poster_url',
    'pubDate': 'valid_date',
    'director': 'directors',
    'actor': 'actors',
}


movie_boxoffice_json_relations = {
    'movieCd':'id',
    'movieNm':'title',
    'openDt':'open_year',
    'salesAcc':'sales',
    'audiAcc':'audience',
}

# movie_data_flow
## 1. 영화 목록 불러오기 (연도, page, etc) => 영화코드, 제목, 영문제목, 개봉연도, 제작연도.
## => 영화코드를 통해 현재 db에 있는지 체크 없다면 상세정보 얻어오기로 넘어가기.
## 2. 상세정보 (영화코드) => 장르 (장르 없다면 생성), 러닝타임, 영화등급, 국가 등 추가.

# actor&director_data_flow
## 1. 영화인 목록
## 2. 영화인상세목록 # 당장 필요하진 않을 수 있음.
## 3. 네이버api를 통해, 배우명(영문도), 배우 사진, 배역 감독명(영문도) 감독 사진 불러오기. (배우 등록할 때 db에 있는지 체크하고 없다면 추가, 배우에 관련영화로 추가),

# boxoffice_data_flow
## 1.
## 2.
## 3.

# TODO : Crawling Code from naver link#
class URL:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        # API urls http://www.kobis.or.kr
        self.daily_boxoffice_base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
        self.weekly_boxoffice_base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
        self.movie_list_base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
        self.movie_detail_base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        self.actor_list_base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json'
        self.actor_detail_base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json'

    def make_url(self, url, **kwargs):
        url = url + '?key=' + self.API_KEY
        for key,val in kwargs.items():
            url += '&{}={}'.format(key, val)
        return url

    def daily_boxoffice_url(self, **kwargs):
        return self.make_url(self.daily_boxoffice_base_url, **kwargs)

    def weekly_boxoffice_url(self, **kwargs):
        return self.make_url(self.weekly_boxoffice_base_url, **kwargs)

    def movie_list_url(self, **kwargs):
        return self.make_url(self.movie_list_base_url, **kwargs)

    def movie_detail_url(self, **kwargs):
        return self.make_url(self.movie_detail_base_url, **kwargs)

    def actor_list_url(self, **kwargs):
        return self.make_url(self.actor_list_base_url, **kwargs)

    def actor_detail_url(self, **kwargs):
        return self.make_url(self.actor_detail_base_url, **kwargs)


class URL_naver:
    def __init__(self, NAVER_ID, NAVER_SECRET):
        self.naver_search_url = 'https://openapi.naver.com/v1/search/movie.json?'
        self.headers = {
            'X-Naver-Client-Id': NAVER_ID,
            'X-Naver-Client-Secret': NAVER_SECRET,
        }

    def make_url(self, url, **kwargs):
        for key, val in kwargs.items():
            url += '&{}={}'.format(key, val)
        return url

    def naver_movie_search_url(self, **kwargs):
        return self.make_url(self.naver_search_url, **kwargs)


class Data:
    def __init__(self, **kwargs):
        '''

        :param kwargs:
        API_KEY : movie_api_key
        NAVER_ID : naver_api_ID
        NAVER_SECRET : naver_api_SECRET
        '''
        self.tr = Json2Json()
        self.url_maker = URL(kwargs['API_KEY'])
        if 'NAVER_ID' in kwargs.keys():
            self.url_maker_naver = URL_naver(kwargs['NAVER_ID'],kwargs['NAVER_SECRET'])
        else:
            self.url_maker_naver = URL_naver("","")

    def get_movie_list(self, num_pages, **kwargs):
        result = []
        if 'flag' in kwargs.keys():
            target_url = self.url_maker.movie_list_url(curPage=num_pages, **kwargs)
            self.tr.set_map(movie_list_json_relations)
            result.extend(self.tr.json2json_list(target_url, method='GET'))
        else:
            for page in range(1, num_pages+1):
                target_url = self.url_maker.movie_list_url(curPage=page, **kwargs)
                self.tr.set_map(movie_list_json_relations)
                result.extend(self.tr.json2json_list(target_url, method='GET'))
        return result

    def get_movie_detail(self, **kwargs):
        target_url = self.url_maker.movie_detail_url(**kwargs)
        self.tr.set_map(movie_detail_json_relations)
        return self.tr.json2json_list(target_url, method='GET')

    def get_actor_list(self, num_pages, **kwargs):
        self.tr.set_map(actor_list_json_relations)
        result = []
        for page in range(1, num_pages+1):
            target_url = self.url_maker.actor_list_url(**kwargs)
            result.extend(self.tr.json2json_list(target_url, method='GET'))
        return result

    def get_actor_detail(self, **kwargs):
        target_url = self.url_maker.actor_detail_url(**kwargs)
        self.tr.set_map(actor_detail_json_relations)
        return self.tr.json2json_list(target_url, method='GET')

    def get_naver_movie(self, name, Dtcheck=None, **kwargs):
        kwargs.update({'query': name})
        target_url = self.url_maker_naver.naver_movie_search_url(**kwargs)
        self.tr.set_map(naver_json_relations)
        result = self.tr.json2json_list(target_url, method='GET', headers=self.url_maker_naver.headers)
        if Dtcheck:
            for obj in result:
                if str(Dtcheck) == obj.get('valid_date'):
                    print('It may be valid, {}'.format(name))
                    return [obj]
            print('There could be no valid data in {}'.format(name))
            return result
        else:
            return self.tr.json2json_list(target_url, method='GET', headers=self.url_maker_naver.headers)


    # TODO 마져 완성하기 => 주간 boxoffice => 영화상세정보 => 받아오기로.
    def get_movie_list_from_boxoffice(self, num, startDt=None,**kwargs):
        result = []
        targetTime = datetime(int(startDt[:4]), int(startDt[4:6]), int(startDt[6:8]))
        self.tr.set_map(movie_boxoffice_json_relations)
        for i in range(num):
            targetTime += TIMEDELTA_A_WEEK
            targetDt = targetTime.strftime('%Y%m%d')
            target_url = self.url_maker.weekly_boxoffice_url(targetDt=targetDt, **kwargs)
            result.extend(self.tr.json2json_list(target_url, method='GET'))
            
        return result

    def get_movie_list_from_boxoffice_daily(self, **kwargs):
        target_url = self.url_maker.daily_boxoffice_base_url(**kwargs)
        return self.tr.json2json_list(target_url, method='GET')

