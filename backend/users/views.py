from django.shortcuts import HttpResponse
from . import models
import json
import os
import hashlib
from django.db import connection


def md5(pwd):
    """
    加盐
    """
    _obj = hashlib.md5()
    _obj.update((pwd + pwd).encode('utf-8'))
    ret = _obj.hexdigest()
    return ret


def register(request):
    data = []
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        student_number = request.POST.get('student_number')
        profile = request.FILES.get('profile')

        if models.Users.objects.filter(user_id=user_id):
            tmp = {
                'status': 404,
                'error': "This ID has been used.",
            }
            data.append(tmp)
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            # 哈希用户密码
            hashed_pwd = md5(password)
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

                models.Users.objects.create(user_id=user_id, username=username, code_hash=hashed_pwd, image_url=profile_link, Real_name_authentication=student_number is not None, user_permissions='user', show_yourself='')

                tmp = {
                    'status': 200,
                    'error': None,
                }
                data.append(tmp)
                return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse(json.dumps(data), content_type='application/json')


def login(request):
    data = []
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            cursor = connection.cursor()
            sql = "select code_hash from users where user_id = {}".format(user_id)
            cursor.execute(sql)
            stored_pwd = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            if md5(password) == stored_pwd[0][0]:
                tmp = {
                    'status': 200,
                    'error': None,
                }
            else:
                tmp = {
                    'status': 404,
                    'error': 'Wrong Password',
                }
            data.append(tmp)
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception as e:
            tmp = {
                'status': 404,
                'error': str(e),
            }
            data.append(tmp)
            return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse(json.dumps(data), content_type='application/json')
