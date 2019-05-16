from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre, Comment, Trailer
from django.db.models import F, Sum, Count, Case, When
from django.http import JsonResponse


def root(request):
    auth_form = AuthenticationForm()
    return render(request, 'movies/root.html',{
        'form': auth_form
    })


def movie_extractor(obj):
    index_pointer = 0
    target = []
    for i in range(3):
        target.append(obj[index_pointer:index_pointer + 6])
        index_pointer += 6
    return target


# TODO 추천 알고리즘 들어가야함.
@login_required
def index(request):
    if request.user.is_authenticated:
        movies = Movie.objects.all()
        # 유저가 체크하지 않은 영화 중 장르 선호도로 추천하기.
        # TODO:유저가 체크하지 않은 영화로 filtering하기.
        genre_preferences = request.user.preferences.all().order_by('-score')
        genre_movie = []
        for gp in genre_preferences:
            genre_movie.extend(gp.genre.movies.all())
        print(genre_movie)

        kinds = []

        # 장르선호도
        kinds.append(movie_extractor(genre_movie))


        return render(request, 'movies/index.html', {
            'kinds': kinds,
        })
    return redirect('root')


@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    # comment는 api 서버로
    return render(request, 'movies/detail.html',{
      'movie': movie
    })


@login_required
def movie_checking(request):
    if request.user.is_authenticated:
        movies = Movie.objects.all()
        return render(request, 'movies/checking.html', {
            'movies': movies
        })
    else:
        return redirect('movies:index')


# TODO: 페이지에 적용시키기 (API 방식으로 작동하여 Vue와 연동할 예정)
@login_required
def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user in comment.liked.all:
        comment.liked.remove(request.user)
        context = {'message': "{} unlike {} comment".format(request.user.username, comment.id)}
    else:
        comment.liked.add(request.user)
        context = {'message': "{} like {} comment".format(request.user.username, comment.id)}

    return JsonResponse(context)


# TODO: Not supposed to do yet.
# TODO: post_lists
def post_list(request, movie_id):
    pass


# TODO:
def post_detail(request, movie_id, post_id):
    pass