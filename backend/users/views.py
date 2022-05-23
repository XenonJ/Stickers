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
        text_or_pic = request.POST.get('text_or_pic')   #判断是图片or文字形式
        picture = request.FILES.get('picture')
        background_url = request.POST.get('background_url')
        text = request.POST.get('text')
        font_size = request.POST.get('font_size')
        font_color = request.POST.get('font_color')
        font_format = request.POST.get('font_format')
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

        background_url = ""  #暂时不知道如何处理

        try:
            post = models.Posts(
                page_coordinates_x=x_coordinate,
                page_coordinates_y=y_coordinate,
                rotation_angle=rotation_angle,
                picture_url=picture_url,
                background_url=background_url,
                text_or_pic=text_or_pic,
                text=text,
                font_size=font_size,
                font_color=font_color,
                font_format=font_format,
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


def notice(request):
    res = {}
    res = json.loads(json.dumps(res))
    if request.method == "GET":
        token = request.GET.get('token')
        data = {}
        data = json.loads((json.dumps(data)))

    try:
        #处理comment
        comments=[]
        num1=0
        usr = models.Users.objects.get(token=token)
        user_id = usr["user_id"]
        Latest_CheckTime=usr["Latest_CheckTime"]   #用户最新活动时间
        psts=models.Posts.objects.filter(user_id=user_id)

        for pst in psts:
            post_id=pst["post_id"]
            picture_url = pst["picture_url"]
            text_or_pic = pst["text_or_pic"]
            text = pst["text"]
            font_size = pst["font_size"]
            font_color = pst["font_color"]
            font_format = pst["font_format"]       #本人发的帖子
            cmts = models.Comments.objects.filter(post_id=post_id)
            for cmt in cmts:
                usr_c = models.Users.objects.get(user_id=cmt["user_id"])# 评论者
                comment_time=cmt["comment_time"]
                comment = cmt["comment"]
                if_anonymous = cmt["if_anonymous"]
                user_name = usr_c["user_name"]
                profile_url = usr_c["image_url"]
                if comment_time.__ge__(Latest_CheckTime):
                    num1=num1+1
                    comments.append({
                        "post_id":post_id,
                        "picture_url":picture_url,
                        "text_or_pic":text_or_pic,
                        "text":text,
                        "font_size":font_size,
                        "font_color":font_color,
                        "font_format": font_format,
                        "comment_time":comment_time,
                        "comment":comment,
                        "if_anonymous":if_anonymous,
                        "user_name":user_name,
                        "image_url":profile_url,
                    })
        data["comments"]=comments


        #处理like_comment
        like_comment=[]
        num2=0
        user_cmts= models.Comments.objects.filter(user_id=user_id)
        for user_cmt in user_cmts:
            usrcomment_id=user_cmt["comment_id"]       #用户自己的评论
            cmtpost_id=user_cmt["post_id"]          #用户的评论所属的帖子id
            pst2 = models.Posts.objects.filter(post_id=cmtpost_id)
            picture_url2 = pst2["picture_url"]
            text_or_pic2 = pst2["text_or_pic"]
            text2 = pst2["text"]
            font_size2 = pst2["font_size"]
            font_color2 = pst2["font_color"]
            font_format2 = pst2["font_format"]
            like_comments=models.LikedComments.objects.filter(comment_id=usrcomment_id)
            for like_comment1 in like_comments:
                likeuser_id=like_comment1["user_id"]
                time=like_comment1["like_time"]
                likeusr=models.Users.objects.filter(user_id=likeuser_id)
                likeuser_name=likeusr["user_name"]
                likeuser_image_url=likeusr["image_url"]
                if time.__ge__(Latest_CheckTime):
                    num2=num2+1
                    like_comment.append({
                        "user_name":likeuser_name,
                        "image_url":likeuser_image_url,
                        "time":time,
                        "comment_id":usrcomment_id,
                        "picture_url": picture_url2,
                        "text_or_pic": text_or_pic2,
                        "text": text2,
                        "font_size": font_size2,
                        "font_color": font_color2,
                        "font_format": font_format2,
                    })
        data["like_comment"]=like_comment

        #处理like_post
        like_post=[]
        num3=0
        psts3=models.Posts.objects.filter(user_id=user_id)

        for pst3 in psts3:
            post_id3 = pst3["post_id"]
            pstlike_num=like_num = models.LikedPosts.objects.filter(post_id=post_id3).count()
            if pstlike_num >0:
                picture_url3 = pst3["picture_url"]
                text_or_pic3 = pst3["text_or_pic"]
                text3 = pst3["text"]
                font_size3 = pst3["font_size"]
                font_color3 = pst3["font_color"]
                font_format3 = pst3["font_format"]
                likedposts=models.LikedPosts.objects.filter(post_id=post_id3)
                for likedpost in likedposts:
                    time3=likedpost["like_time"]    #点赞时间
                    likepost_user_id=likedpost["user_id"]
                    usr3=models.Users.objects.filter(user_id=likepost_user_id)
                    user_name3=usr3["user_name"]
                    image_url3=usr3["image_url"]
                    if  time3.__ge__(Latest_CheckTime):
                        num3=num3+1
                        like_post.append({
                            "user_name":user_name3,
                            "image_url":image_url3,
                            "time":time3,
                            "post_id":post_id3,
                            "picture_url":picture_url3,
                            "text_or_pic": text_or_pic3,
                            "text": text3,
                            "font_size": font_size3,
                            "font_color": font_color3,
                            "font_format": font_format3,
                        })
        data["like_post"]=like_post
        sum=num1+num2+num3
        data["sum"]=sum

        res["data"] = data
        res["status"] = 200
        res["error"] = ""

    except Exception as e:
        res["status"] = 404
        res["error"] = e

    return HttpResponse(json.dumps(res), content_type='application/json')
