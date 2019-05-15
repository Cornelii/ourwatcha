from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse

from .models import User

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
        return render(request, 'accounts/forms.html', {
            'form': form,
            'button_message': '가입하기',
        })


def login(request):
    if request.method == 'POST':
        auth_form = AuthenticationForm(request, request.POST)
        if auth_form.is_valid():
            print(get_user_model())
            auth_login(request, auth_form.get_user())
            return redirect('movies:index')
    else:
        auth_form = AuthenticationForm()
    return render(request, 'accounts/forms.html', {
        'form': auth_form,
        'button_message': '로그인하기'
    })


def logout(request):
    auth_logout(request)
    return redirect('root')


def withdraw(request):
    pass


@login_required
def profile(request, user_name):
    if request.user.is_authenticated:
        user = get_user_model()
        people = user.loving_people.all()

        followings = user.followings.all()
        movies = user.checking.all()
        return render(request, 'accounts/profile.html',{
            'people': people,
            'followings': followings,
            'movies': movies,
        })


@login_required()
def follow(request, user_id): # user_it to follow
    if request.user.is_authenticated:
        target_user = get_object_or_404(User, pk=user_id)
        user = get_user_model()
        if user in target_user.followed.all():
            # 팔로잉 중 이므로 팔로잉 취소.
            user.followings.remove(target_user)
            follow_status = False
        else:
            # 팔로잉!
            user.followings.add(target_user)
            follow_status = True
        return JsonResponse({
            'follow': follow_status
        })
    return JsonResponse({
        'message': "인증되지 않은 사용자입니다."
    })


@login_required
def change(request):
    if request.user.is_authenticated:
        user = get_user_model()
        if request.method == 'POST':
            pass
        else:
            form = CustomUserChangeForm(instance=user)
            return render(request, 'accounts/forms.html', {
                'form': form,
                'button_message': '변경하기',
            })

