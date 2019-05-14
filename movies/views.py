from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Genre, Comment, Trailer
import requests

# TODO: rootPage
def root(request):
    return render(request, 'movies/root.html')


# TODO: Create your views here.
def index(request):
    movies = Movie.objects.all()
    print(movies)
    return render(request, 'movies/index.html', {
        'movies':movies
    })


# TODO: movie detail page
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    # comment는 api 서버로
    return render(request, 'movies/detail.html',{
      'movie': movie
    })


# TODO: Not supposed to do yet.
# TODO: post_lists
def post_list(request, movie_id):
    pass


# TODO:
def post_detail(request, movie_id, post_id):
    pass