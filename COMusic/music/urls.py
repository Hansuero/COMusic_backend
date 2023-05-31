# music/urls.py
from django.urls import path
from music.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('upload_song', upload_song),
    path('delete_song', delete_song),
    path('create_new_favo', create_new_favo),
    path('get_favo_list', get_favo_list),
    path('add_song_to_favo', add_song_to_favo),
    path('get_songs_in_favo', get_songs_in_favo),
    path('add_to_recent', add_to_recent),
    path('post_max', post_max),
    path('get_record_list', get_record_list),
    path('get_uploaded_list', get_uploaded_list),

]
