from django.contrib import admin
from .models import Movie, Comment, Genre, Trailer

admin.site.register(Movie)

admin.site.register(Comment)

admin.site.register(Genre)

admin.site.register(Trailer)