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

    return HttpResponse(json.dumps(res), content_type='application/json')


def myself(request):
    res = {}
    res = json.loads(json.dumps(res))

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
