from django.db import models


class Role(models.Model):
    type_name = models.CharField(max_length=20)


class People(models.Model):
    code = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=45)
    en_name = models.CharField(max_length=45, blank=True)
    filmography = models.TextField(blank=True)

    class Meta:
        abstract = True


class Director(People):
    portrait_url = models.CharField(max_length=200, null=True)
    roles = models.ManyToManyField(Role, related_name='directors')


class Actor(People):
    portrait_url = models.CharField(max_length=200, null=True)
    roles = models.ManyToManyField(Role, related_name='actors')


class Staff(People):
    roles = models.ManyToManyField(Role, related_name='staffs')

