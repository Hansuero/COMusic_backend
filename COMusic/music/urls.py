# music/urls.py
from django.urls import path
from music.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('upload_song', upload_song),
    path('delete_song', delete_song),


]