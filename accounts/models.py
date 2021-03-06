from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from people.models import People
from movies.models import Movie, Genre, Comment


class User(AbstractUser):
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed')
    checking = models.ManyToManyField(Movie, related_name='checked')
    loving_people = models.ManyToManyField(People, related_name="loved")
    like_comment = models.ManyToManyField(Comment, related_name="liked")

    def is_my_star(self, person):
        if not isinstance(person, People):
            return

        if person in self.loving_people.all():
            return Temperature.objects.get(star=person.id)


class Temperature(models.Model):
    temp = models.IntegerField(default=0)
    movie_click = models.IntegerField(default=0, null=True)
    portrait_click = models.IntegerField(default=0, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temps')
    person = models.ForeignKey(People, on_delete=models.CASCADE, related_name='temps')

    def click_movie(self):
        self.movie_click += 1
    
    def click_portrait(self):
        self.portrait_click += 1

    def temp_update(self):
        self.temp = self.movie_click + 2*self.portrait_click


class GenrePreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='preferences')
    score = models.IntegerField(default=0)




