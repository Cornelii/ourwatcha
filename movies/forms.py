from django import forms
from .models import Movie, Genre, Comment, Trailer


class MovieModelForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = '__all__'


class GenreModelForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = '__all__'


class CommentModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'


class TrailerModelForm(forms.ModelForm):
    class Meta:
        model = Trailer
        fields = '__all__'
