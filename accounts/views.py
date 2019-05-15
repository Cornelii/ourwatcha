from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash

from .forms import CustomUserCreationForm


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')

        # print error message (error reason) on signup page
        print(form._errors.get_json_data())
        for _, each_field_errors in form._errors.get_json_data().items():
            for error in each_field_errors:
                messages.warning(request, error.get('message'))

        return redirect('accounts:signup')

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

def change(request):
    pass