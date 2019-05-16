from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre, Comment, Trailer
from accounts.models import GenrePreference
from django.db.models import F, Sum, Count, Case, When
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

def root(request):
    auth_form = AuthenticationForm()
    return render(request, 'movies/root.html',{
        'form': auth_form
    })


def movie_extractor(obj):
    index_pointer = 0
    target = []
    for i in range(5):
        tmp_obj = obj[index_pointer:index_pointer + 6]
        if tmp_obj:
            target.append(tmp_obj)
            index_pointer += 6
        else:
            break
    return target


# TODO 추천 알고리즘 들어가야함.
@login_required
def index(request):
    if request.user.is_authenticated:
        # 유저가 체크하지 않았다면, 체킹창으로 유도,
        user = request.user
        gps = user.preferences.all()
        if gps:
            pass
        else:
            messages.success(request, '먼저 영화에 평점을 매겨주세요. 많이 평점을 매기실 수록 기호에 맞는 영화를 찾으실 수 있습니다.')
            return redirect('movies:movie_checking')
        movies = Movie.objects.all()
        kinds = []

        # 유저가 체크하지 않은 영화 중 장르 선호도로 추천하기.
        # TODO:유저가 체크하지 않은 영화로 filtering하기.
        genre_preferences = request.user.preferences.all().order_by('-score')
        genre_movie = []
        for gp in genre_preferences:
            genre_movie.extend(gp.genre.movies.all())

        # 장르선호도
        kinds.append(movie_extractor(genre_movie))

        # 온도가 높은 영화인이 있는 영화.
        try:
            tmps_movie = []
            tmp = user.temps.order_by('-temp').first()

            tmps_movie.extend(tmp.person.movies.all())
            kinds.append(movie_extractor(tmps_movie))
        except:
            pass

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
        user = request.user
        print('what')
        checked_movies = user.checking.all()
        print(checked_movies)
        checked_id = []
        for movie in checked_movies:
            checked_id.append(movie.id)
        # TODO sql caching 고려하기
        movies = Movie.objects.filter(~Q(id__in=checked_id))
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