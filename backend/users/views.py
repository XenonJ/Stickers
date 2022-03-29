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

                models.Users.objects.create(user_id=user_id, user_name=user_name, code_hash=hashed_pwd, token=token, image_url=profile_link, Real_name_authentication=student_number is not None, user_permissions='user', show_yourself='')

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
            cmt = models.Comments(user_id=user_id, post_id=post_id, comment=content, if_anonymous=if_anonymous)
            cmt.save()

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
            models.LikedPosts.objects.create(user_id=user_id, post_id=post_id)

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
            models.LikedComments.objects.create(user_id=user_id, comment_id=comment_id)

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
    return HttpResponse(json.dumps(res), content_type='application/json')


def rename(request):
    res = {}
    res = json.loads(json.dumps(res))
    return HttpResponse(json.dumps(res), content_type='application/json')


def change_profile(request):
    res = {}
    res = json.loads(json.dumps(res))
    return HttpResponse(json.dumps(res), content_type='application/json')


def delete_comment(request):
    res = {}
    res = json.loads(json.dumps(res))
    return HttpResponse(json.dumps(res), content_type='application/json')


def rm_like_post(request):
    res = {}
    res = json.loads(json.dumps(res))
    return HttpResponse(json.dumps(res), content_type='application/json')


def rm_like_comment(request):
    res = {}
    res = json.loads(json.dumps(res))
    return HttpResponse(json.dumps(res), content_type='application/json')


def delete_post(request):
    res = {}
    res = json.loads(json.dumps(res))
    return HttpResponse(json.dumps(res), content_type='application/json')
