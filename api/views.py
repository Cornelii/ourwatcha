from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .serializers import MovieSerializer, CommentSerializer, GenreSerializer
from .serializers import PeopleSerializer
from movies.models import Movie, Comment, Genre
from people.models import People
from accounts.models import Temperature, GenrePreference
from django.http import JsonResponse

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = MovieSerializer(movie, many=False)
    return Response(serializer.data)


# TODO 포스트 쪽에 평점 연결.
@api_view(['GET', 'POST'])
def comment_list(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            print(request.user.id)
            request.data.update(user=request.user.id)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()  # 평점이 등록되는 순간
                # 유저와 영화를 연결
                user = request.user
                user.checking.add(movie)
                # 기존 해당 장르선호도 존재하는지 확인.(복수개의 장르가 존재 가능)
                genres = movie.genre.all()
                for genre in genres:
                    try:
                        gp = GenrePreference.objects.get(Q(user_id=request.user.id) & Q(genre_id=genre.id))
                    except:
                        # 없다면 장르선호도 생성
                        gp = GenrePreference.objects.create(user_id=request.user.id, genre=genre)
                    # 평점에 따라 스코어 부여
                    user_score = int(request.data.get('score'))
                    if user_score < 5:
                        gp.score -= user_score
                    else:
                        gp.score += user_score
                    gp.save()
                return Response(serializer.data)
        else:
            return Response({'message': '인증되지 않은 사용자입니다.'})
    else:
        comments = movie.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


# TODO 평점 적용 method.
@api_view(['GET', 'POST'])
def star_scoring(request, movie_id):
    print('hit')
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        print('hit')
        if request.user.is_authenticated:
            user = request.user
            # 체킹한 영화에 추가.
            user.checking.add(movie)
            print(user.checking.all())
            # 기존 해당 장르선호도 존재하는지 확인.(복수개의 장르가 존재 가능)
            genres = movie.genre.all()
            for genre in genres:
                try:
                    gp = GenrePreference.objects.get(Q(user_id=request.user.id) & Q(genre_id=genre.id))
                except:
                    # 없다면 장르선호도 생성
                    gp = GenrePreference.objects.create(user_id=request.user.id, genre=genre)
                # 평점에 따라 스코어 부여
                user_score = int(request.data.get('score'))
                if user_score < 5:
                    gp.score -= user_score
                else:
                    gp.score += user_score
                gp.save()
            return Response({'message': '평점이 적용되었습니다.'})
        else:
            return Response({'message': '인증되지 않은 사용자입니다.'})
    else:
        comments = movie.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)



@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, movie_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'GET':
        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        return Response({'message': '해당 평점이 삭제되었습니다.'})
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    return Response({'message': '유효한 방법을 통해 요청하세요.'})


@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = genre.movies.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def people(request):
    people = People.objects.all()
    serializer = PeopleSerializer(people, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def people_detail(request, actor_id):
    people = get_object_or_404(People, pk=actor_id)
    serializer = PeopleSerializer(people, many=False)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def movie_click_up(request, movie_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            movie = get_object_or_404(Movie,pk=movie_id)
            peoples = movie.people.all()
            for person in peoples:
                # 순회하며 해당 영화인과의 온도가 있는지 확인하고, 없다면 생성해서 가져오기
                try:
                    temp = user.temps.filter(Q(person_id__exact=person.id))[0]
                except:
                    temp = Temperature.objects.create(user=user, person_id=person.id)
                temp.click_movie()
                temp.temp_update()
                temp.save()
            return JsonResponse({'message': '성공적으로 업데이트 되었습니다.'})
    return JsonResponse({'message': "검증되지 않은 사용자입니다."})


@api_view(['GET', 'POST'])
def portrait_click_up(request, people_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # 유저와 해당 영화인의 온도가 있는지 확인하고, 가져오기, 없다면 생성
            user = request.user
            try:
                temp = user.temps.get(Q(person_id__exact=people_id))
            except:
                temp = Temperature.objects.create(user=user, person_id=people_id)
            # 온도를 가져와서 portrait_click_up
            temp.click_portrait()
            temp.temp_update()
            temp.save()
            return JsonResponse({'message': '성공적으로 업데이트 되었습니다.'})
    return JsonResponse({'message': "검증되지 않은 사용자입니다."})



#TODO 목록을 모아서 한번에 업데이트 하는 함수 정의 (localStorage)