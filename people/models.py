from django.db import models


class Role(models.Model):
    type_name = models.CharField(max_length=20)


class People(models.Model):
    code = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=45)
    en_name = models.CharField(max_length=45, blank=True)
    filmography = models.TextField(blank=True)
    portrait_url = models.CharField(max_length=200, null=True)
    roles = models.ManyToManyField(Role, related_name='peoples')