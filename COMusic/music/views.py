import os

from django.http import JsonResponse
from django.shortcuts import render

from COMusic.settings import BASE_DIR
from music.models import Song, UserUploadSong, Playlist
from user.models import User


# Create your views here.
def upload_song(request):
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    if request.method == 'POST':
        username = request.session['username']
        user = User.objects.get(username=username)
        song_name = request.POST.get('song_name')
        song_tag = request.POST.get('song_tag')
        song_cover = request.FILES.get('song_cover')
        singer = request.POST.get('singer')
        lyric = request.POST.get('lyric', '')  # 默认为空
        song_file = request.FILES.get('song_file')  # 获取上传的歌曲文件

        if song_file:  # 如果上传了歌曲文件
            _, ext = os.path.splitext(song_file.name)
            # 生成歌曲文件的保存路径
            song_path = os.path.join(BASE_DIR, 'song', f'{user.id}_song{ext}')

            # 保存歌曲文件到指定路径
            with open(song_path, 'wb') as file:
                for chunk in song_file.chunks():
                    file.write(chunk)
            song = Song.objects.create(song_name=song_name, song_tag=song_tag, song_url=song_path, lyric=lyric,
                                       singer=singer)
            if song_cover:  # 如果上传了封面
                _, ext = os.path.splitext(song_cover.name)
                song_cover_path = os.path.join(BASE_DIR, 'song_cover', f'{song_name}_song_cover{ext}')
                song.song_cover_url = song_cover_path
                song.save()

                with open(song_cover_path, 'wb') as file:
                    for chunk in song_cover.chunks():
                        file.write(chunk)
            UserUploadSong.objects.create(user=user, song=song)
            result = {'result': 0, 'message': r'上传歌曲成功！'}
            return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def delete_song(request):
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    if request.method == 'POST':
        username = request.session['username']
        user = User.objects.get(username=username)
        song_name = request.POST.get('song_name')

        # 根据歌曲名和用户查找对应的上传歌曲记录
        user_upload_songs = UserUploadSong.objects.filter(user=user, song__song_name=song_name)

        if user_upload_songs.exists():
            # 遍历匹配的上传歌曲记录，逐个删除
            for user_upload_song in user_upload_songs:
                song_path = user_upload_song.song.song_url

                # 删除歌曲文件和上传歌曲记录
                if os.path.exists(song_path):
                    os.remove(song_path)
                user_upload_song.song.delete()
                user_upload_song.delete()

            result = {'result': 0, 'message': r'删除歌曲成功！'}
            return JsonResponse(result)
        else:
            result = {'result': 0, 'message': r'未找到对应的上传歌曲记录！'}
            return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def create_new_favo(request):
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)
    if request.method == 'POST':
        playlist_name = request.POST.get('favo_title')
        user = User.objects.get(username=request.session['username'])
        new_favo = Playlist.objects.create(user=user, playlist_name=playlist_name)
        result = {'result': 0, 'message': r'创建收藏夹成功！', 'favo_id': new_favo.id,
                  'favo_title': new_favo.playlist_name}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)
