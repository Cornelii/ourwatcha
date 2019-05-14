from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash


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


def profile(request):
    pass

def change(request):
    pass