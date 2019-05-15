from django.shortcuts import render, redirect, get_object_or_404
from .models import People
from django.contrib.auth.decorators import login_required


#TODO people pages
def index(request):
    people = People.objects.all()

    return render(request, 'people/index.html', {
        'people': people,
    })


def people_detail(request, people_id):
    person = get_object_or_404(People, pk=people_id)
    filmo = person.filmography
    filmo = filmo.split('|')
    return render(request, 'people/detail.html',{
        'person': person,
        'filmo': filmo,
    })
