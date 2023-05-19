import re

from django.http import JsonResponse
from django.shortcuts import redirect

from user.models import *


# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if len(username) == 0 or len(password1) == 0 or len(password2) == 0:
            result = {'result': 0, 'message': r'用户名与密码不允许为空!'}
            return JsonResponse(result)

        if User.objects.filter(username=username).exists():
            result = {'result': 0, 'message': r'用户已存在!'}
            return JsonResponse(result)

        if password1 != password2:
            result = {'result': 0, 'message': r'两次密码不一致!'}
            return JsonResponse(result)

        email = request.POST.get('email', '')

        if len(email) == 0:
            result = {'result': 0, 'message': r'邮箱不允许为空!'}
            return JsonResponse(result)
        User.objects.create(username=username, password=password1, email=email)
        result = {'result': 0, 'message': r'注册成功!'}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username):
            result = {'result': 0, 'message': r'查无此人！'}
            return JsonResponse(result)
        user = User.objects.get(username=username)
        if user.password == password:
            request.session['username'] = username
            request.session.set_expiry(3600)
            result = {'result': 0, 'message': r'登录成功！'}
            return JsonResponse(result)
        else:
            result = {'result': 0, 'message': r'密码错误！'}
            return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def logout(request):
    request.session.flush()
    result = {'result': 0, 'message': r'注销成功！'}
    return JsonResponse(result)


def upload_bio(request):
    if request.method == 'POST':
        user = request.user
        bio = request.POST.get('bio')
        if len(bio) > 256:
            result = {'result': 0, 'message': r'个人简介长度超过限制！'}
            return JsonResponse(result)
        user.bio = bio
        user.save()
        result = {'result': 0, 'message': r'上传成功！'}
        return JsonResponse(result)
        ##return redirect('profile')  # 重定向到用户的个人资料页面
    else:
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)