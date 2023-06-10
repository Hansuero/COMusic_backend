# super_admin/urls.py
from django.urls import path
from super_admin.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('get_report_list', get_report_list),
    path('complain_song', complain_song),
    path('complain_playlist', complain_playlist),
]