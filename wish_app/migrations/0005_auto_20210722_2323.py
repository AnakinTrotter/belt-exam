# Generated by Django 2.2.5 on 2021-07-23 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish_app', '0004_auto_20210722_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='users_who_like',
            field=models.ManyToManyField(related_name='liked_wishes', to='wish_app.User'),
        ),
    ]
