# Generated by Django 4.0 on 2022-04-19 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='likedcomments',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='likedposts',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='posts',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'managed': False},
        ),
    ]