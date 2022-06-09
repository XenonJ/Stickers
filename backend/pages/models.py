from django.db import models


# Create your models here.
class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=100)
    token = models.CharField(max_length=500)
    user_name = models.CharField(max_length=20, blank=False)
    code_hash = models.CharField(max_length=20, blank=False)
    image_url = models.URLField()
    Real_name_authentication = models.BooleanField(default=False)
    Student_id = models.IntegerField(default=0)
    user_permissions = models.CharField(max_length=20)
    show_yourself = models.CharField(max_length=100)
    Latest_CheckTime=models.TimeField(auto_now=True)

    class Meta:
        # managed = False
        db_table = 'users'


class Posts(models.Model):
    post_id = models.IntegerField(primary_key=True)
    post_time = models.TimeField(auto_now_add=True)
    page_coordinates_x = models.IntegerField(default=None)
    page_coordinates_y = models.IntegerField(default=None)
    rotation_angle = models.IntegerField(default=0)
    background_url = models.URLField()
    text_or_pic=models.BooleanField(default=True)
    picture_url = models.URLField()

    text = models.CharField(max_length=500)
    font_size = models.CharField(max_length=500)
    font_color = models.CharField(max_length=500)
    font_format = models.CharField(max_length=500)

    if_anonymous = models.BooleanField(default=False)
    # post_user_id=models.CharField(max_length=50)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, default='', db_column='user_id')
    latest_ActTime = models.TimeField(auto_now=True)

    class Meta:
        db_table='posts'




class Comments(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    comment = models.CharField(max_length=500, default='')
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id')
    if_anonymous = models.BooleanField(default=False)
    post_id = models.ForeignKey('Posts', on_delete=models.CASCADE, db_column='post_id')
    # like_number = models.IntegerField()
    comment_time = models.TimeField(default=None)

    class Meta:
        # managed = False
        db_table = 'comments'


class LikedPosts(models.Model):
    post_id = models.ForeignKey('Posts', on_delete=models.CASCADE, db_column='post_id')
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id')
    like_time = models.TimeField(auto_now_add=True)

    class Meta:
        # managed = False
        unique_together = ("post_id", "user_id")


class LikedComments(models.Model):
    comment_id = models.ForeignKey('Comments', on_delete=models.CASCADE, db_column='comment_id')
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id')
    like_time = models.TimeField(auto_now_add=True)

    class Meta:
        # managed = False
        unique_together = ("comment_id", "user_id")

