# Generated by Django 2.1.7 on 2019-05-13 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='running_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
