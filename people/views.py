from django.shortcuts import render, redirect, get_object_or_404
from .models import Director, Actor, Staff
from django.contrib.auth.decorators import login_required

# Create your views here.

# TODO: people page
def index(request):
    directors = Director.objects.all()
    actors = Actor.objects.all()
    staff = Staff.objects.all()

    return render(request, 'people/index.html', {
        'directors': directors,
        'actors': actors,
        'staff': staff,
    })

# TODO: director list page
def director_list(request):
    directors = Director.objects.all()

    return render(request, 'people/index.html', {
        'directors': directors,
        'actors': {},
        'staff': {},
    })

# TODO: actor list page
def actor_list(request):
    actors = Actor.objects.all()

    return render(request, 'people/index.html', {
        'directors':{},
        'actors': actors,
        'staff': {},
    })

# TODO: staff list page
def staff_list(request):
    staff = Staff.objects.all()

    return render(request, 'people/index.html', {
        'directors': {},
        'actors': {},
        'staff': staff,
    })

# TODO: director detail page
def director_detail(request, director_id):
    person = get_object_or_404(Director, pk=director_id)
    status = '감독'
    return render(request, 'people/detail.html',{
        'person': person,
        'status':status
    })

# TODO: actor detail page
def actor_detail(request, actor_id):
    person = get_object_or_404(Actor, pk=actor_id)
    status = '배우'
    return render(request, 'people/detail.html', {
        'person': person,
        'status': status
    })

# TODO: staff detail page
def staff_detail(request, staff_id):
    person = get_object_or_404(Staff, pk=staff_id)
    status = '스태프'
    return render(request, 'people/detail.html', {
        'person': person,
        'status': status
    })

