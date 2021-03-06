# Generated by Django 2.1.7 on 2019-05-13 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
        ('people', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.IntegerField(blank=True)),
                ('movie_click', models.IntegerField(blank=True)),
                ('portrait_click', models.IntegerField(blank=True)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temps', to='people.Actor')),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temps', to='people.Director')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temps', to='people.Staff')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='loving_actors',
            field=models.ManyToManyField(related_name='loved', to='people.Actor'),
        ),
        migrations.AddField(
            model_name='user',
            name='loving_directors',
            field=models.ManyToManyField(related_name='loved', to='people.Director'),
        ),
        migrations.AddField(
            model_name='user',
            name='loving_staffs',
            field=models.ManyToManyField(related_name='loved', to='people.Staff'),
        ),
        migrations.AddField(
            model_name='user',
            name='watch',
            field=models.ManyToManyField(related_name='watched', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='temperature',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temps', to=settings.AUTH_USER_MODEL),
        ),
    ]
