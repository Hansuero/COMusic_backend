from django.http import JsonResponse
from django.shortcuts import render
from music.models import Song, Playlist
from user.models import User


# Create your views here.
def search_song(request):
    if request.method == 'GET':
        song_name = request.GET.get('song_name')
        if song_name:
            song_list = Song.objects.filter(song_name__icontains=song_name)
            if song_list:
                song_list_data = [s.to_dic() for s in song_list]
                result = {'result': 0, 'message': r'搜索成功！', 'song_list': song_list_data}
                return JsonResponse(result)
            else:
                result = {'result': 3, 'message': r'无结果！'}
                return JsonResponse(result)
        else:
            result = {'result': 4, 'message': r'关键词不能为空！'}
            return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def search_playlist(request):
    if request.method == 'GET':
        playlist_name = request.GET.get('songlist_name')
        if playlist_name:
            playlist_list = Playlist.objects.filter(playlist_name__icontains=playlist_name, is_shared=True)
            if playlist_list:
                playlist_list_data = [p.to_dic() for p in playlist_list]
                result = {'result': 0, 'message': r'搜索成功！', 'songlist_list': playlist_list_data}
                return JsonResponse(result)
            else:
                result = {'result': 3, 'message': r'无结果！'}
                return JsonResponse(result)
        else:
            result = {'result': 4, 'message': r'关键词不能为空！'}
            return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def search_user(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        if username:
            user_list = User.objects.filter(username__icontains=username)
            if user_list:
                user_list_data = [u.to_dic() for u in user_list]
                result = {'result': 0, 'message': r'搜索成功！', 'user_list': user_list_data}
                return JsonResponse(result)
            else:
                result = {'result': 3, 'message': r'无结果！'}
                return JsonResponse(result)
        else:
            result = {'result': 4, 'message': r'关键词不能为空！'}
            return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def get_recommend_song(request):
    if request.method == 'GET':
        song_tag = request.GET.get('song_tag')
        if song_tag:
            # 获取 10 个符合tag的歌曲列表
            song_list = Song.objects.filter(song_tag=song_tag)[0:10]
            if song_list:
                song_data = [s.to_simple_dic() for s in song_list]
                result = {'result': 0, 'message': r'返回推荐列表成功！', 'song_data': song_data}
                return JsonResponse(result)
            else:
                result = {'result': 3, 'message': r'无结果！'}
                return JsonResponse(result)
        else:
            result = {'result': 2, 'message': r'标签不能为空！'}
            return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def get_recommend_playlist(request):
    if request.method == 'GET':
        playlist_tag = request.GET.get('playlist_tag')
        if playlist_tag:
            # 获取 10 个符合tag的歌单列表
            playlist_list = Playlist.objects.filter(playlist_tag=playlist_tag, is_shared=True)[0:10]
            if playlist_list:
                playlist_data = [p.to_simple_dic() for p in playlist_list]
                result = {'result': 0, 'message': r'返回推荐列表成功！', 'playlist_data': playlist_data}
                return JsonResponse(result)
            else:
                result = {'result': 3, 'message': r'无结果！'}
                return JsonResponse(result)
        else:
            result = {'result': 2, 'message': r'标签不能为空！'}
            return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)
