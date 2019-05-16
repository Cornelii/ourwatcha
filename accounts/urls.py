from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<str:username/>', views.profile, name='profile'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('followcheck/<int:user_id>/', views.follow_check, name='follow_check'),
    path('change/', views.change, name='change'),
]
