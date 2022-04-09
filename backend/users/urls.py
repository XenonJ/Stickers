from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('upload_post/', views.upload_post),
    path('comment/', views.comment),
    path('like_post/', views.like_post),
    path('like_comment', views.like_comment),
    path('show_yourself/', views.show_yourself),
    path('rename/', views.rename),
    path('change_profile/', views.change_profile),
    path('delete_comment/', views.delete_comment),
    path('rm_like_post/', views.rm_like_post),
    path('rm_like_comment/', views.rm_like_comment),
    path('delete_post/', views.delete_post),
    path('comment/', views.comment),
]
