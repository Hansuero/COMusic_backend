# comment/urls.py
from django.urls import path
from comment.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('create_comment', create_comment),
    path('delete_comment', delete_comment),
    path('change_comment', change_comment),
    path('get_comment', get_comment),
]