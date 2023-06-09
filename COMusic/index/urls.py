# index/urls.py
from django.urls import path
from index.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('search_song', search_song),
    path('search_playlist', search_playlist),
    path('search_user', search_user),
    path('get_recommend_song', get_recommend_song),
    path('get_recommend_playlist', get_recommend_playlist),
]