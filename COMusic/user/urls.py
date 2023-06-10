# user/urls.py
from django.urls import path
from user.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('upload_intro', upload_intro),
    path('upload_photo', upload_photo),
    path('show_following', show_following),
    path('follow_user', follow_user),
    path('unfollow_user', unfollow_user),
    path('get_user_info', get_user_info),
    path('get_other_info', get_other_info),
    path('get_intro', get_intro),
    path('get_other_intro', get_other_intro),
]