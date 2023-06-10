import os
import re

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404

from COMusic.settings import BASE_DIR
from user.models import *
from music.models import *

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if len(username) == 0 or len(password1) == 0 or len(password2) == 0:
            result = {'result': 2, 'message': r'用户名与密码不允许为空！'}
            return JsonResponse(result)

        if User.objects.filter(username=username).exists():
            result = {'result': 3, 'message': r'用户已存在！'}
            return JsonResponse(result)

        if password1 != password2:
            result = {'result': 4, 'message': r'两次密码不一致！'}
            return JsonResponse(result)

        email = request.POST.get('email', '')

        if len(email) == 0:
            result = {'result': 5, 'message': r'邮箱不允许为空！'}
            return JsonResponse(result)
        photo_url = os.path.join(BASE_DIR, 'photo', 'default.jpg')
        
        user = User.objects.create(username=username, password=password1, email=email, photo_url=photo_url)
        like = Playlist.objects.create(user=user, playlist_name='我喜欢', is_shared=False)
        user.like_id = like.id
        user.save()
        request.session['username'] = username
        request.session.set_expiry(3600)
        result = {'result': 0, 'message': r'注册成功！'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r"请求方式错误！"}
        return JsonResponse(result)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username):
            result = {'result': 2, 'message': r'查无此人！'}
            return JsonResponse(result)
        user = User.objects.get(username=username)
        if user.password == password:
            request.session['username'] = username
            request.session.set_expiry(3600)
            result = {'result': 0, 'message': r'登录成功！'}
            return JsonResponse(result)
        else:
            result = {'result': 3, 'message': r'密码错误！'}
            return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def logout(request):
    request.session.flush()
    result = {'result': 0, 'message': r'注销成功！'}
    return JsonResponse(result)


def upload_intro(request):
    if 'username' not in request.session:  # 检查用户是否已登录
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)
    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        intro = request.POST.get('intro')
        if len(intro) > 256:
            result = {'result': 3, 'message': r'个人简介长度超过限制！'}
            return JsonResponse(result)
        user.intro = intro
        user.save()
        result = {'result': 0, 'message': r'上传成功！'}
        return JsonResponse(result)
        # return redirect('profile')  # 重定向到用户的个人资料页面
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def upload_photo(request):
    if 'username' not in request.session:  # 检查用户是否已登录
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)
    if request.method == 'POST':
        username = request.session['username']
        user = User.objects.get(username=username)
        photo = request.FILES.get('photo')  # 获取上传的头像文件

        if photo:  # 如果上传了头像文件
            # 生成头像文件的保存路径
            _, ext = os.path.splitext(photo.name)
            photo_path = os.path.join(BASE_DIR, 'photo', f'{user.id}_photo{ext}')

            # 保存头像文件到指定路径
            with open(photo_path, 'wb') as file:
                for chunk in photo.chunks():
                    file.write(chunk)

            # 更新用户的头像路径
            user.photo_url = photo_path
            user.photo_url_out = 'http://82.157.165.72:8888/photo/' + f'{user.id}_photo{ext}'
            user.save()
            result = {'result': 0, 'message': r'上传头像成功！'}
            return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def show_following(request):
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)
    if request.method == 'GET':
        username = request.session['username']
        user = User.objects.get(username=username)
        following = Follow.objects.filter(follower=user)
        following_list = [{'username': follow.following.username, 'user_id': follow.following.id, 'photo_url': follow.following.photo_url_out} for follow in following]

        result = {'result': 0, 'message': r'获取关注列表成功！', 'following': following_list}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def follow_user(request):
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)

    if request.method == 'POST':
        username = request.session['username']
        user = User.objects.get(username=username)
        following_username = request.POST.get('following_username')

        try:
            following_user = User.objects.get(username=following_username)
        except User.DoesNotExist:
            result = {'result': 3, 'message': r'用户不存在！'}
            return JsonResponse(result)

        if Follow.objects.filter(follower=user, following=following_user).exists():
            result = {'result': 4, 'message': r'已关注该用户！'}
            return JsonResponse(result)

        # 创建关注关系
        follow = Follow.objects.create(follower=user, following=following_user)

        result = {'result': 0, 'message': r'成功关注用户！'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def unfollow_user(request):
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)

    if request.method == 'DELETE':
        username = request.session['username']
        user = User.objects.get(username=username)
        following_username = request.GET.get('following_username')
        try:
            following_user = User.objects.get(username=following_username)
        except User.DoesNotExist:
            result = {'result': 3, 'message': r'用户不存在！'}
            return JsonResponse(result)

        follow = Follow.objects.filter(follower=user, following=following_user).first()
        if not follow:
            result = {'result': 4, 'message': r'未关注该用户！'}
            return JsonResponse(result)

        # 取消关注
        follow.delete()

        result = {'result': 0, 'message': r'成功取消关注！'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def get_user_info(request):
    if request.method == 'GET':
        username = request.session['username']
        user_data = User.objects.get(username=username).to_dic()
        result = {'result': 0, 'message': r"返回成功", 'user_data': user_data}
        return JsonResponse(result)

    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def get_other_info(request):
    if request.method == 'GET':
        user_id = request.GET.get('id')
        user_data = User.objects.get(id=user_id).to_dic()
        result = {'result': 0, 'message': r"返回成功", 'user_data': user_data}
        return JsonResponse(result)

    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def get_intro(request):
    if request.method == 'GET':
        username = request.session['username']
        user_data = User.objects.get(username=username).intro
        result = {'result': 0, 'message': r"返回成功", 'intro': user_data}
        return JsonResponse(result)

    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)
    

def get_other_intro(request):
    if request.method == 'GET':
        user_id = request.GET.get('id')
        user_data = User.objects.get(id=user_id).intro
        result = {'result': 0, 'message': r"返回成功", 'intro': user_data}
        return JsonResponse(result)

    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)