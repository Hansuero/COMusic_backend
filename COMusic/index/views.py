from django.http import JsonResponse
from django.shortcuts import render
from music.models import Song
from user.models import User


# Create your views here.
def search_song(request):
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)
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
