from django.urls import path
from . import views
app_name = 'people'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:people_id>/', views.people_detail, name='people_detail'),
    path('fan/<int:people_id>/', views.be_fan),
    path('fancheck/<int:people_id>/', views.check_be_fan),
]