import datetime
import time

from django.shortcuts import HttpResponse
from . import models
import json
import os
import hashlib


def main_page(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "GET":
        token = request.GET.get('token')

        data = {}
        data = json.loads((json.dumps(data)))

        try:
            # 处理posts
            posts = models.Posts.objects.filter(latest_ActTime__gte=datetime.datetime.now() + datetime.timedelta(hours=-48))
            ls = []
            for post in posts:
                ls.append({
                    "post_id": post["post_id"],
                    "x_coordinates": post["page_coordinates_x"],
                    "y_coordinates": post["page_coordinates_y"],
                    "rotation_angle": post["rotation_angle"],
                    "picture_url": post["picture_url"],
                    "background_url": post["background_url"],
                })
            data["posts"] = ls

            # 处理user
            usr = models.Users.objects.filter(token=token)
            user_name = usr[0]["user_name"]
            profile_url = usr[0]["image_url"]
            data["user"] = {
                "user_name": user_name,
                "profile_url": profile_url,
            }
            res["data"] = data
            res["status"] = 200
            res["error"] = ""

        except Exception as e:
            res["status"] = 404
            res["error"] = e

    return HttpResponse(json.dumps(res), content_type='application/json')


def myself(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "GET":
        token = request.GET.get('token')

        data = {}
        data = json.loads((json.dumps(data)))

        try:
            # 处理user
            usr = models.Users.objects.filter(token=token)
            user_name = usr[0]["user_name"]
            profile_url = usr[0]["image_url"]
            show_yourself = usr[0]["show_yourself"]
            data["user"] = {
                "user_name": user_name,
                "profile_url": profile_url,
                "show_yourself": show_yourself,
            }

            # 处理likes
            likes = {}
            likes = json.loads(json.dumps(likes))

            # 处理likes_posts
            posts = models.LikedPosts.objects.filter(user_id=usr[0]["user_id"])
            ls = []
            for post in posts:
                picture_url = models.Posts.objects.get(post_id=post["post_id"])["picture_url"]
                ls.append({
                    "post_id": post["post_id"],
                    "picture_url": picture_url,
                    "like_time": post["like_time"]
                })
            likes["posts"] = ls

            # 处理likes_comments
            cmts = models.LikedComments.objects.filter(user_id=usr[0]["user_id"])
            ls = []
            for cmt in cmts:
                comment = models.Comments.objects.get(comment_id=cmt["comment_id"])["comment"]
                ls.append({
                    "comment_id": cmt["comment_id"],
                    "comment": comment,
                    "like_time": cmt["like_time"]
                })
            likes["comments"] = ls

            data["likes"] = likes

            # 处理comments
            cmts = models.Comments.objects.filter(user_id=usr[0]["user_id"])

        except Exception as e:
            res["status"] = 404
            res["error"] = e

    return HttpResponse(json.dumps(res), content_type='application/json')


def user_detail(request):
    res = {}
    res = json.loads(json.dumps(res))

    return HttpResponse(json.dumps(res), content_type='application/json')


def notice(request):
    res = {}
    res = json.loads(json.dumps(res))

    return HttpResponse(json.dumps(res), content_type='application/json')


def post_detail(request):
    res = {}
    res = json.loads(json.dumps(res))

    return HttpResponse(json.dumps(res), content_type='application/json')
