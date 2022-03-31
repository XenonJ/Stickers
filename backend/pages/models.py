# from django.db import models
#
#
# # Create your models here.
# class Users(models.Model):
#     user_id = models.IntegerField(primary_key=True)
#     user_name = models.CharField(max_length=20, blank=False)
#     code_hash = models.CharField(max_length=20, blank=False)
#     image_url = models.URLField()
#     Real_name_authentication = models.BooleanField(default=False)
#     Student_id = models.IntegerField(default=0)
#     user_permissions = models.CharField(max_length=20)
#     show_yourself = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = 'users'
#
#
# class Posts(models.Model):
#     post_id = models.IntegerField(primary_key=True)
#     post_time = models.TimeField(auto_now_add=True)
#     page_coordinates_x = models.IntegerField(default=None)
#     page_coordinates_y = models.IntegerField(default=None)
#     rotation_angle = models.IntegerField(default=0)
#     picture_url = models.URLField()
#     background_url = models.URLField()
#     # like_number = models.IntegerField()
#     # comment_number = models.IntegerField()
#     if_anonymous = models.BooleanField(default=False)
#     # post_user_id=models.CharField(max_length=50)
#     user_id = models.ForeignKey('Users', on_delete=models.CASCADE, default=0)
#
#     class Meta:
#         db_table = 'posts'
#
#
# class Comments(models.Model):
#     comment_id = models.IntegerField(primary_key=True)
#     comment = models.CharField(max_length=500, default='')
#     user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
#     if_anonymous = models.BooleanField(default=False)
#     post_id = models.ForeignKey('Posts', on_delete=models.CASCADE)
#     # like_number = models.IntegerField()
#     comment_time = models.TimeField(default=None)
#
#     class Meta:
#         db_table = 'comments'
#
#
# class LikedPosts(models.Model):
#     post_id = models.ForeignKey('Posts', on_delete=models.CASCADE)
#     user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
#     like_time = models.TimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ("post_id", "user_id")
#
#
# class LikedComments(models.Model):
#     comment_id = models.ForeignKey('Comments', on_delete=models.CASCADE)
#     user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
#     like_time = models.TimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ("comment_id", "user_id")
