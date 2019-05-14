from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/comments/', views.comment_list, name='comment_list'),
    path('movies/<int:movie_id>/comments/<int:comment_id>/', views.comment_detail, name='comment_detail'),

    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:genre_id>/movies/', views.genre_movies, name='genre_movies'),

    path('people/actors/', views.actors, name='actors'),
    path('people/directors/', views.directors, name='directors'),
    path('people/staff/', views.staff, name='staff'),

    path('people/actors/<int:actor_id>', views.actor_detail, name='actor_detail'),
    path('people/directors/<int:director_id>', views.director_detail, name='director_detail'),
    path('people/staff/<int:staff_id>', views.staff_detail, name='staff_detail'),

    #TODO user-people temperatrue api


    #TODO query-type rest api url
]