from django.contrib import admin
from .models import Temperature, GenrePreference, User
# Register your models here.

admin.site.register(User)

admin.site.register(Temperature)

admin.site.register(GenrePreference)

