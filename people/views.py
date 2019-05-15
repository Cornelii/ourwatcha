from django.shortcuts import render, redirect, get_object_or_404
from .models import People
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse

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


@login_required
def be_fan(request, people_id):
    if request.user.is_authenticated:
        person = get_object_or_404(People, pk=people_id)
        user = get_user_model()

        if user in person.loved.all(): # fan임
            # fan취소
            user.loving_people.remove(person)
            fan = False
        else:
            user.loving_people.add(person)
            fan = True
        return JsonResponse({
            'fan': fan
        })
    else:
        return JsonResponse({'message':'인증 되지 않은 사용자입니다.'})
