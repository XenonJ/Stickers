# Generated by Django 3.2.5 on 2022-03-23 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='comment_time',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='like_number',
        ),
    ]