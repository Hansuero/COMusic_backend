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
    path('get_max', get_max),
    path('post_max', post_max),
    path('get_record_list', get_record_list),
    path('get_uploaded_list', get_uploaded_list),
    path('set_shared', set_shared),
    path('unshare_songlist', unshare_songlist),
    path('add_songs_to_favo', add_songs_to_favo),
    path('get_playlist', get_playlist),
    path('get_song', get_song),
    path('cancel_favo', cancel_favo),
    path('delete_list', delete_list),
	path('add_i_like', add_i_like),
	path('cancel_i_like', cancel_i_like),
 	path('get_is_shared', get_is_shared),
]
