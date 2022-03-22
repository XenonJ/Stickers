from django.db import models


# Create your models here.
class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=20)
    code_hash = models.CharField(max_length=20)
    image_url = models.CharField(max_length=20)
    Real_name_authentication = models.BooleanField()
    user_permissions = models.CharField(max_length=20)
    show_yourself = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'


class Posts(models.Model):
    post_id = models.IntegerField(primary_key=True)
    post_time = models.CharField(max_length=50)
    page_coordinates = models.CharField(max_length=50)
    rotation_angle = models.IntegerField()
    picture_url = models.CharField(max_length=50)
    background_url = models.CharField(max_length=50)
    like_number = models.IntegerField()
    comment_number = models.IntegerField()
    if_anonymous = models.BooleanField()
    post_user_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'posts'


class Comments(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    if_anonymous = models.BooleanField()
    post_id = models.IntegerField()
    like_number = models.IntegerField()
    comment_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'comments'


class LikedPosts(models.Model):
    post_id = models.IntegerField()
    user_id = models.IntegerField()
    like_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'liked_posts'


class CommentedPosts(models.Model):
    post_id = models.IntegerField()
    user_id = models.IntegerField()
    comment_time = models.CharField(max_length=50)

    class Meta:
        db_table = 'commented_posts'
