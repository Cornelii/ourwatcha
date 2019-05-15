from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from people.models import People
from movies.models import Movie, Genre


class User(AbstractUser):
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed')
    checking = models.ManyToManyField(Movie, related_name='checked')
    loving_people = models.ManyToManyField(People, related_name="loved")


class Temperature(models.Model):
    temp = models.IntegerField(default=0)
    movie_click = models.IntegerField(blank=True, null=True)
    portrait_click = models.IntegerField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temps')
    person = models.ForeignKey(People, on_delete=models.CASCADE, related_name='temps')


class GenrePreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='preferences')
    score = models.IntegerField(default=0)




