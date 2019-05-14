from django.db import models
from django.conf import settings
from people.models import Director, Actor, Staff


class Genre(models.Model):
    type_name = models.CharField(max_length=20, unique=True)


class Movie(models.Model):
    # 초기 api 요청 시 채워지는 필드
    id = models.IntegerField(primary_key=True, unique=True) # movieCode
    title = models.CharField(max_length=140)
    en_title = models.CharField(max_length=140, blank=True)
    open_year = models.CharField(max_length=8, blank=True)
    prdt_year = models.CharField(max_length=8, blank=True)

    # detail api 요청 시 채워지는 필드
    running_time = models.IntegerField(blank=True, null=True)
    nation = models.CharField(max_length=50, blank=True)
    grade = models.CharField(max_length=10, blank=True)

    genre = models.ManyToManyField(Genre, related_name="movies")

    # detil api로 업데이트 되는 필드
    state = models.CharField(max_length=10, blank=True)

    # movie - boxoffice 업데이트 시 채워지는 필드
    audience = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    sales = models.IntegerField(blank=True, null=True)


    # naver 업데이트 시 채워지는 필드
    description = models.TextField(blank=True)
    poster_url = models.CharField(max_length=200, blank=True)

    # 기타 관계형 필드
    actors = models.ManyToManyField(Actor, related_name='movies')
    directors = models.ManyToManyField(Director, related_name='movies')
    staffs = models.ManyToManyField(Staff, related_name='movies')


class Comment(models.Model):
    content = models.CharField(max_length=5000)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Trailer(models.Model):
    trailer_url = models.CharField(max_length=200, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='trailers')

