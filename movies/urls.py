from django.urls import path
from . import views
app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('checks/', views.movie_checking, name='movie_checking'),

    #path('<int:movie_id>/comments/', views.comments, name='comments'),
    #path('<int:movie_id>/comments/<int:comment_id>', views.comment_detail, name='comment_detail'),
    #path('<int:movie_id>/comments/<int:comment_id>/like/', views.comment_like, name='comment_like'),

    # 아직 구현 안됨 (개인 포스팅)
    path('<int:movie_id>/posts/', views.post_list, name='post_list'),
    path('<int:movie_id>/posts/<int:post_id>', views.post_detail, name='post_detail'),

]