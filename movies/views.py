from django.shortcuts import render
import requests

# TODO: Create your views here.
def index(request):
    return render(request, 'movies/index.html')


# TODO: movie detail page
def movie_detail(request, movie_id):
    pass



# TODO: Not supposed to do yet.
# TODO: post_lists
def post_list(request, movie_id):
    pass


# TODO:
def post_detail(request, movie_id, post_id):
    pass