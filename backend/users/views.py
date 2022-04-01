import time

from django.shortcuts import HttpResponse
from . import models
import json
import os
import hashlib


def md5(pwd):
    """
    加盐
    """
    _obj = hashlib.md5()
    _obj.update((pwd + pwd).encode('utf-8'))
    ret = _obj.hexdigest()
    return ret


def register(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        student_number = request.POST.get('student_number')
        profile = request.FILES.get('profile')

        if models.Users.objects.filter(user_id=user_id):
            res['status'] = 404
            res['error'] = "This ID has been used."
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            # 用户密码加盐
            hashed_pwd = md5(password)
            # 生成用户token
            token = md5(user_id + password)
            # 修改头像图片名称
            profile.name = user_id + profile.name

            if profile is not None:
                if not os.path.exists('images'):
                    os.mkdir('images')
                with open(os.path.join(os.getcwd(), 'images', profile.name), 'wb') as fw:
                    # 分块读取
                    for ck in profile.chunks():
                        fw.write(ck)
                profile_link = os.path.join('http://127.0.0.1:8000/', 'images/' + profile.name)

                models.Users.objects.create(
                    user_id=user_id,
                    user_name=user_name,
                    code_hash=hashed_pwd,
                    token=token,
                    image_url=profile_link,
                    Real_name_authentication=student_number is not None,
                    user_permissions='user',
                    show_yourself=''
                )

                res['status'] = 200
                res['error'] = ""
                return HttpResponse(json.dumps(res), content_type='application/json')
    return HttpResponse(json.dumps(res), content_type='application/json')


def login(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            usr = models.Users.objects.filter(user_id=user_id)
            if md5(password) == usr[0]["code_hash"]:
                data = {
                    'token': usr[0]["token"],
                    'user_permission': usr[0]["user_permissions"]
                }
                res['data'] = data
                res['status'] = 200
                res['error'] = ""
            else:
                res['status'] = 404
                res['error'] = "Wrong Password."
            return HttpResponse(json.dumps(res), content_type='application/json')

        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')
    return HttpResponse(json.dumps(res), content_type='application/json')


def upload_post(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        x_coordinate = request.POST.get('x_coordinate')
        y_coordinate = request.POST.get('y_coordinate')
        rotation_angle = request.POST.get('rotation_angle')
        picture = request.FILES.get('picture')
        background_selection = request.POST.get('background_selection')
        if_anonymous = request.POST.get('if_anonymous')

        # 获取token值对应的user_id
        usr = models.Users.objects.filter(token=token)
        user_id = usr[0]["user_id"]

        # 修改图片名称
        picture.name = str(time.time()) + picture.name

        # 存储上传图片
        with open(os.path.join(os.getcwd(), 'images', picture.name), 'wb') as fw:
            for ck in picture.chunks():
                fw.write(ck)
            picture_url = os.path.join('http://127.0.0.1:8000/', 'images/' + picture.name)

        background_url = ""

        try:
            post = models.Posts(
                page_coordinates_x=x_coordinate,
                page_coordinates_y=y_coordinate,
                rotation_angle=rotation_angle,
                picture_url=picture_url,
                background_url=background_url,
                if_anonymous=if_anonymous,
                user_id=user_id
            )
            post.save()

        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    res['status'] = 200
    res['error'] = ""
    return HttpResponse(json.dumps(res), content_type='application/json')


def comment(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        if_anonymous = request.POST.get('if_anonymous')

        # 获取token值对应的user_id
        usr = models.Users.objects.filter(token=token)
        user_id = usr[0]["user_id"]

        try:
            cmt = models.Comments(
                user_id=user_id,
                post_id=post_id,
                comment=content,
                if_anonymous=if_anonymous
            )
            cmt.save()

            # 保存该帖子的最后更改时间
            models.Posts.objects.get(post_id=post_id).save()

        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    res['status'] = 200
    res['error'] = ""
    return HttpResponse(json.dumps(res), content_type='application/json')


def like_post(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        post_id = request.POST.get('post_id')

        # 获取token值对应的user_id
        usr = models.Users.objects.filter(token=token)
        user_id = usr[0]["user_id"]

        try:
            models.LikedPosts.objects.create(
                user_id=user_id,
                post_id=post_id
            )

            # 保存该帖子的最后更改时间
            models.Posts.objects.get(post_id=post_id).save()

        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    res['status'] = 200
    res['error'] = ""
    return HttpResponse(json.dumps(res), content_type='application/json')


def like_comment(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        comment_id = request.POST.get('comment_id')

        # 获取token值对应的user_id
        usr = models.Users.objects.filter(token=token)
        user_id = usr[0]["user_id"]

        try:
            models.LikedComments.objects.create(
                user_id=user_id,
                comment_id=comment_id
            )

            # 获取评论对应的帖子id
            cmt = models.Comments.objects.get(comment_id=comment_id)
            post_id = cmt["post_id"]

            # 保存该帖子的最后更改时间
            models.Posts.objects.get(post_id=post_id).save()

        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    res['status'] = 200
    res['error'] = ""
    return HttpResponse(json.dumps(res), content_type='application/json')


def show_yourself(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        show_yourself_str = request.POST.get('show_yourself')

        try:
            models.Users.objects.filter(token=token).update(show_yourself=show_yourself_str)
        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    res['status'] = 200
    res['error'] = ""
    return HttpResponse(json.dumps(res), content_type='application/json')


def rename(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        user_name = request.POST.get('user_name')

        try:
            models.Users.objects.filter(token=token).update(user_name=user_name)
        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    res['status'] = 200
    res['error'] = ""
    return HttpResponse(json.dumps(res), content_type='application/json')


def change_profile(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        profile = request.FILES.get('profile')

        # 修改图片名称
        profile.name = str(time.time()) + profile.name

        # 存储上传图片
        with open(os.path.join(os.getcwd(), 'images', profile.name), 'wb') as fw:
            for ck in profile.chunks():
                fw.write(ck)
            picture_url = os.path.join('http://127.0.0.1:8000/', 'images/' + profile.name)

        try:
            models.Users.objects.filter(token=token).update(image_url=picture_url)
        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    res['status'] = 200
    res['error'] = ""

    return HttpResponse(json.dumps(res), content_type='application/json')


def delete_comment(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        comment_id = request.POST.get('comment_id')

        # 获取token值对应的user_id
        usr = models.Users.objects.filter(token=token)
        user_id = usr[0]["user_id"]

        try:
            cmt = models.Comments.objects.filter(comment_id=comment_id)
            if cmt[0]["user_id"] == user_id:
                cmt.delete()
                res['status'] = 200
                res['error'] = ""
            else:
                res['status'] = 404
                res['error'] = "Wrong token"

        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    return HttpResponse(json.dumps(res), content_type='application/json')


def rm_like_post(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        post_id = request.POST.get('post_id')

        # 获取token值对应的user_id
        usr = models.Users.objects.filter(token=token)
        user_id = usr[0]["user_id"]

        try:
            cmt = models.LikedPosts.objects.filter(post_id=post_id)
            if cmt[0]["user_id"] == user_id:
                cmt.delete()
                res['status'] = 200
                res['error'] = ""
            else:
                res['status'] = 404
                res['error'] = "Wrong token"

        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    return HttpResponse(json.dumps(res), content_type='application/json')


def rm_like_comment(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        comment_id = request.POST.get('comment_id')

        # 获取token值对应的user_id
        usr = models.Users.objects.filter(token=token)
        user_id = usr[0]["user_id"]

        try:
            cmt = models.LikedComments.objects.filter(comment_id=comment_id)
            if cmt[0]["user_id"] == user_id:
                cmt.delete()
                res['status'] = 200
                res['error'] = ""
            else:
                res['status'] = 404
                res['error'] = "Wrong token"

        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    return HttpResponse(json.dumps(res), content_type='application/json')


def delete_post(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "POST":
        token = request.POST.get('token')
        post_id = request.POST.get('post_id')

        # 获取token值对应的user_id
        usr = models.Users.objects.filter(token=token)
        user_id = usr[0]["user_id"]

        try:
            cmt = models.Posts.objects.filter(post_id=post_id)
            if cmt[0]["user_id"] == user_id:
                cmt.delete()
                res['status'] = 200
                res['error'] = ""
            else:
                res['status'] = 404
                res['error'] = "Wrong token"

        except Exception as e:
            res['status'] = 404
            res['error'] = str(e)
            return HttpResponse(json.dumps(res), content_type='application/json')

    return HttpResponse(json.dumps(res), content_type='application/json')
