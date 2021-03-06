# Generated by Django 3.2.5 on 2022-06-09 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=500)),
                ('user_name', models.CharField(max_length=20)),
                ('code_hash', models.CharField(max_length=20)),
                ('image_url', models.URLField()),
                ('Real_name_authentication', models.BooleanField(default=False)),
                ('Student_id', models.IntegerField(default=0)),
                ('user_permissions', models.CharField(max_length=20)),
                ('show_yourself', models.CharField(max_length=100)),
                ('Latest_CheckTime', models.TimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('post_id', models.IntegerField(primary_key=True, serialize=False)),
                ('post_time', models.TimeField(auto_now_add=True)),
                ('page_coordinates_x', models.IntegerField(default=None)),
                ('page_coordinates_y', models.IntegerField(default=None)),
                ('rotation_angle', models.IntegerField(default=0)),
                ('background_url', models.URLField()),
                ('text_or_pic', models.BooleanField(default=True)),
                ('picture_url', models.URLField()),
                ('text', models.CharField(max_length=500)),
                ('font_size', models.CharField(max_length=500)),
                ('font_color', models.CharField(max_length=500)),
                ('font_format', models.CharField(max_length=500)),
                ('if_anonymous', models.BooleanField(default=False)),
                ('latest_ActTime', models.TimeField(auto_now=True)),
                ('user_id', models.ForeignKey(db_column='user_id', default='', on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
            options={
                'db_table': 'posts',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('comment', models.CharField(default='', max_length=500)),
                ('if_anonymous', models.BooleanField(default=False)),
                ('comment_time', models.TimeField(default=None)),
                ('post_id', models.ForeignKey(db_column='post_id', on_delete=django.db.models.deletion.CASCADE, to='users.posts')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='LikedPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_time', models.TimeField(auto_now_add=True)),
                ('post_id', models.ForeignKey(db_column='post_id', on_delete=django.db.models.deletion.CASCADE, to='users.posts')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
            options={
                'unique_together': {('post_id', 'user_id')},
            },
        ),
        migrations.CreateModel(
            name='LikedComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_time', models.TimeField(auto_now_add=True)),
                ('comment_id', models.ForeignKey(db_column='comment_id', on_delete=django.db.models.deletion.CASCADE, to='users.comments')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
            options={
                'unique_together': {('comment_id', 'user_id')},
            },
        ),
    ]
