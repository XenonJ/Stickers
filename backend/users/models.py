from django.db import models


# Create your models here.
class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=20,blank=False)
    code_hash = models.CharField(max_length=20,blank=False)
    image_url = models.URLField(max_length=20)
    Real_name_authentication = models.BooleanField(default=False)
    Student_id=models.IntegerField(default=0)
    user_permissions = models.CharField(max_length=20)
    show_yourself = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'


class Posts(models.Model):
    post_id = models.IntegerField(primary_key=True)
    post_time = models.TimeField()
    page_coordinates = models.CharField(max_length=50,blank=False)
    rotation_angle = models.IntegerField(default=0)
    picture_url = models.URLField (max_length=50)
    background_url = models.URLField (max_length=50)
    # like_number = models.IntegerField()
    # comment_number = models.IntegerField()
    if_anonymous = models.BooleanField(default=False)
    # post_user_id=models.CharField(max_length=50)
    user_id = models.ForeignKey('Users',on_delete=models.CASCADE,default=0)

    class Meta:
        db_table = 'posts'


class Comments(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    comment = models.CharField(max_length=500,default='')
    user_id = models.ForeignKey('Users',on_delete=models.CASCADE)
    if_anonymous = models.BooleanField(default=False)
    post_id = models.ForeignKey('Posts',on_delete=models.CASCADE)
    like_number = models.IntegerField()
    comment_time = models.TimeField()

    class Meta:
        db_table = 'comments'


class LikedPosts(models.Model):
    post_id = models.ForeignKey('Posts',on_delete=models.CASCADE)
    user_id = models.ForeignKey('Users',on_delete=models.CASCADE)
    like_time = models.TimeField()

    class Meta:
        unique_together = ("post_id", "user_id")


class CommentedPosts(models.Model):
    post_id = models.ForeignKey('Posts',on_delete=models.CASCADE)
    user_id = models.ForeignKey('Users',on_delete=models.CASCADE)
    comment_time = models.TimeField()

    class Meta:
        unique_together = ("post_id", "user_id")
