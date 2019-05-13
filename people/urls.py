from django.urls import path
from . import views
app_name = 'people'

urlpatterns = [
    path('', views.index, name='index'),
    path('directors/', views.director_list, name='director_list'),
    path('actors/', views.actor_list, name='actor_list'),
    path('staff/', views.staff_list, name='staff_list'),
    path('directors/<int:director_id>/', views.director_detail, name='director_detail'),
    path('actors/<int:actor_id>/', views.actor_detail, name='actor_detail'),
    path('staff/<int:staff_id>/', views.staff_detail, name='staff_detail'),

]