from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre, Comment, Trailer


# TODO: rootPage
def root(request):
    auth_form = AuthenticationForm()
    return render(request, 'movies/root.html',{
        'form': auth_form
    })


# TODO: Create your views here.
@login_required
def index(request):
    if request.user.is_authenticated:
        movies = Movie.objects.all()
        print(movies)
        return render(request, 'movies/index.html', {
            'movies':movies
        })
    return redirect('root')


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