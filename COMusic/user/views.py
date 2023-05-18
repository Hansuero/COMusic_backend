import re

from django.http import JsonResponse
from user.models import *


# Create your views here.

def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if len(user_name) == 0 or len(password1) == 0 or len(password2) == 0:
            result = {'result': 0, 'message': r'用户名与密码不允许为空!'}
            return JsonResponse(result)

        if User.objects.filter(user_name=user_name).exists():
            result = {'result': 0, 'message': r'用户已存在!'}
            return JsonResponse(result)

        if password1 != password2:
            result = {'result': 0, 'message': r'两次密码不一致!'}
            return JsonResponse(result)

        email = request.POST.get('email', '')

        if len(email) == 0:
            result = {'result': 0, 'message': r'邮箱不允许为空!'}
            return JsonResponse(result)
        User.objects.create(user_name=user_name, password=password1, email=email)
        result = {'result': 0, 'message': r'注册成功!'}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)
