from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth import update_session_auth_hash

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request, request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = UserCreationForm()
        return render(request, 'accounts/forms.html', {
            'form': form
        })

def login(request):
    pass


def logout(request):
    auth_logout(request)
    return redirect('root')


def withdraw(request):
    pass


def profile(request):
    pass

def change(request):
    pass