# Generated by Django 2.1.8 on 2019-05-17 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_like_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperature',
            name='movie_click',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='portrait_click',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
