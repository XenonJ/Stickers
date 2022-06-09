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
            # posts = models.Posts.objects.filter(latest_ActTime__gte=datetime.datetime.now() + datetime.timedelta(hours=-48))
            posts = models.Posts.objects.all()
            ls = []
            for post in posts:
                ls.append({
                    "post_id": post.post_id,
                    "x_coordinates": post.page_coordinates_x,
                    "y_coordinates": post.page_coordinates_y,
                    "rotation_angle": post.rotation_angle,
                    "picture_url": post.picture_url,
                    "background_url": post.background_url,
                    "text_or_pic":post.text_or_pic,
                    "text":post.text,
                    "font_size":post.font_size,
                    "font_color":post.font_color,
                    "font_format":post.font_format,
                })
            data["posts"] = ls

            # 处理user
            usr = models.Users.objects.filter(token=token)
            user_name = usr[0].user_name
            profile_url = usr[0].image_url
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
            usr = models.Users.objects.get(token=token)
            user_name = usr.user_name
            profile_url = usr.image_url
            show_yourself = usr.show_yourself
            data["user"] = {
                "user_name": user_name,
                "profile_url": profile_url,
                "show_yourself": show_yourself,

            }

            # 处理posts
            posts = []
            psts = models.Posts.objects.filter(user_id=usr["user_id"]).order_by("-post_time")
            num = min(4, psts.count())
            for i in range(num):
                posts.append({
                    "post_id": psts[i].post_id,
                    "picture_url": psts[i].picture_url,
                    "post_time": psts[i].post_time,
                    "text_or_pic": psts[i].text_or_pic,
                    "text": psts[i].text,
                    "font_size": psts[i].font_size,
                    "font_color": psts[i].font_color,
                    "font_format": psts[i].font_format,
                })
            data["posts"] = posts

            res["data"] = data
            res["status"] = 200
            res["error"] = ""

        except Exception as e:
            res["status"] = 404
            res["error"] = e

    return HttpResponse(json.dumps(res), content_type='application/json')


def user_detail(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        data = {}
        data = json.loads((json.dumps(data)))

        try:
            # 处理user
            usr = models.Users.objects.get(user_id=user_id)
            user_name = usr.user_name
            profile_url = usr.image_url
            show_yourself = usr.show_yourself
            data["user"] = {
                "user_name": user_name,
                "profile_url": profile_url,
                "show_yourself": show_yourself,
            }

            # 处理posts
            posts = []
            psts = models.Posts.objects.filter(user_id=usr["user_id"]).order_by("-post_time")
            num = min(4, psts.count())
            for i in range(num):
                posts.append({
                    "post_id": psts[i].post_id,
                    "picture_url": psts[i].picture_url,
                    "post_time": psts[i].post_time,
                    "text_or_pic": psts[i].text_or_pic,
                    "text": psts[i].text,
                    "font_size": psts[i].font_size,
                    "font_color": psts[i].font_color,
                    "font_format": psts[i].font_format,
                })
            data["posts"] = posts

            res["data"] = data
            res["status"] = 200
            res["error"] = ""

        except Exception as e:
            res["status"] = 404
            res["error"] = e

    return HttpResponse(json.dumps(res), content_type='application/json')


def post_detail(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "GET":
        token = request.GET.get('token')
        post_id = request.GET.get('post_id')
        data = {}
        data = json.loads((json.dumps(data)))

        try:
            # 处理post
            pst = models.Posts.objects.filter(post_id=post_id)[0]
            usr_s = models.Users.objects.filter(token=token)[0]   # 浏览者
            usr_p = models.Users.objects.filter(user_id=pst.user_id.user_id)[0]   # 发帖人
            cmts = models.Comments.objects.filter(post_id=post_id)

            if_self = (usr_p.user_id == usr_s.user_id)
            post_time = pst.post_time
            picture_url = pst.picture_url
            background_url = pst.background_url
            like_num = models.LikedPosts.objects.filter(post_id=pst).count()
            print(1)
            comment_num = cmts.count()
            if_anonymous = pst.if_anonymous
            user_id = usr_p.user_id
            user_name = usr_p.user_name
            profile_url = usr_p.image_url
            text_or_pic = pst.text_or_pic
            text = pst.text
            font_size = pst.font_size
            font_color = pst.font_color
            font_format = pst.font_format

            data["post"] = {
                "if_self": if_self,
                "post_time": post_time,
                "picture_url": picture_url,
                "background_url": background_url,
                "like_num": like_num,
                "comment_num": comment_num,
                "if_anonymous": if_anonymous,
                "user_id": user_id,
                "user_name": user_name,
                "profile_url": profile_url,
                "text_or_pic":text_or_pic,
                "text":text,
                "font_size":font_size,
                "font_color":font_color,
                "font_format":font_format,
            }

            # 处理comments
            comments = []
            for cmt in cmts:
                usr_c = models.Users.objects.get(user_id=cmt.user_id)    # 评论者

                if_self = usr_s.user_id == usr_c.user_id
                comment_id = cmt.comment_id
                comment_time = cmt.comment_time
                comment = cmt.comment
                like_num = models.LikedComments.objects.filter(comment_id=comment_id).count()
                if_anonymous = cmt.if_anonymous
                user_id = usr_c.user_id
                user_name = usr_c.user_name
                profile_url = usr_c.image_url

                comments.append({
                    "if_self": if_self,
                    "comment_id": comment_id,
                    "comment_time": comment_time,
                    "comment": comment,
                    "like_num": like_num,
                    "if_anonymous": if_anonymous,
                    "user_id": user_id,
                    "user_name": user_name,
                    "profile_url": profile_url,
                })
            data["comments"] = comments

            res["data"] = data
            res["status"] = 200
            res["error"] = ""

        except Exception as e:
            res["status"] = 404
            res["error"] = e

    return HttpResponse(json.dumps(res), content_type='application/json')
