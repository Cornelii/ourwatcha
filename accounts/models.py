from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from people.models import Director, Actor, Staff
from movies.models import Movie, Genre


class User(AbstractUser):
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed')
    checking = models.ManyToManyField(Movie, related_name='checked')
    loving_actors = models.ManyToManyField(Actor, related_name="loved")
    loving_directors = models.ManyToManyField(Director, related_name="loved")
    loving_staffs = models.ManyToManyField(Staff, related_name='loved')


class Temperature(models.Model):
    temp = models.IntegerField(default=0)
    movie_click = models.IntegerField(blank=True, null=True)
    portrait_click = models.IntegerField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temps')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='temps')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='temps')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='temps')


class GenrePreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='preferences')
    score = models.IntegerField(default=0)




