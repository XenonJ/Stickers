from django.urls import path
from . import views

urlpatterns = [
    path('main_page/', views.main_page),
    path('myself/', views.myself),
    path('user_detail/', views.user_detail),
    path('post_detail/', views.post_detail),
]
