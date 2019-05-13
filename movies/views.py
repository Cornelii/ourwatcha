from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    return render(request, 'movies/index.html')




# database update
def db_update(request):
    pass