from django.contrib import admin
from .models import Role, Director, Actor, Staff
# Register your models here.

admin.site.register(Role)

admin.site.register(Director)

admin.site.register(Actor)

admin.site.register(Staff)