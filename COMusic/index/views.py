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
        playlist_name = request.GET.get('playlist_name')
        if playlist_name:
            playlist_list = Playlist.objects.filter(playlist_name__icontains=playlist_name)
            if playlist_list:
                playlist_list_data = [p.to_dic() for p in playlist_list]
                result = {'result': 0, 'message': r'搜索成功！', 'playlist_list': playlist_list_data}
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
