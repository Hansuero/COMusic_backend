import os

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from COMusic.settings import BASE_DIR
from music.models import Song, UserUploadSong, Playlist, PlaylistSong, RecentPlay
from user.models import User
from utils.utils import *


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
        if singer == '':
            singer = '佚名'
        lyric = request.POST.get('lyric', '')  # 默认为空
        song_file = request.FILES.get('song_file')  # 获取上传的歌曲文件

        if song_file:  # 如果上传了歌曲文件
            _, ext = os.path.splitext(song_file.name)
            # 生成歌曲文件的保存路径
            song = Song.objects.create(song_name=song_name, song_tag=song_tag, lyric=lyric,
                                       singer=singer)
            song_path = os.path.join(BASE_DIR, 'song', f'{song.id}_song{ext}')
            song.song_url = song_path
            song.save()
            # 保存歌曲文件到指定路径
            with open(song_path, 'wb') as file:
                for chunk in song_file.chunks():
                    file.write(chunk)

            if song_cover:  # 如果上传了封面
                _, ext = os.path.splitext(song_cover.name)
                song_cover_path = os.path.join(BASE_DIR, 'song_cover', f'{song.id}_song_cover{ext}')
                song.song_cover_url = song_cover_path
                song.save()

                with open(song_cover_path, 'wb') as file:
                    for chunk in song_cover.chunks():
                        file.write(chunk)
            else:
                song.song_cover_url = os.path.join(BASE_DIR, 'song_cover', 'default.jpg')
                song.save()
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

    if request.method == 'DELETE':
        username = request.session['username']
        user = User.objects.get(username=username)
        song_id = request.GET.get('song_id')
        song = Song.objects.get(id=song_id)
        # 根据歌曲id和用户id查找对应的上传歌曲记录
        user_upload_songs = UserUploadSong.objects.filter(user=user, song=song)

        if user_upload_songs.exists():
            # 遍历匹配的上传歌曲记录，逐个删除
            for user_upload_song in user_upload_songs:
                song_path = user_upload_song.song.song_url

                # 删除歌曲文件和上传歌曲记录
                if os.path.exists(song_path):
                    os.remove(song_path)
                song_name = user_upload_song.song.song_name
                # 系统给用户发一条消息提示删除成功
                content = '您上传的歌曲 ' + song_name + ' 删除成功！'
                create_report(get_admin(), user, content)
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


def get_favo_list(request):
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)
    if request.method == 'GET':
        user = User.objects.get(username=request.session['username'])
        playlists = Playlist.objects.filter(user=user)
        playlists_data = [{'favo_id': p.id, 'favo_title': p.playlist_name} for p in playlists]
        result = {'result': 0, 'message': r'获取收藏夹成功！', 'playlists': playlists_data}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def add_song_to_favo(request):
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        song_id = request.POST.get('song_id')
        playlist_id = request.POST.get('playlist_id')

        try:
            song = Song.objects.get(id=song_id)
            playlist = Playlist.objects.get(id=playlist_id)
            if playlist.user.id != user.id:
                result = {'result': 0, 'message': r'您的名下不存在该歌单！'}
                return JsonResponse(result)
        except (Song.DoesNotExist, Playlist.DoesNotExist):
            result = {'result': 0, 'message': r'歌曲或歌单不存在！'}
            return JsonResponse(result)

        playlist_song = PlaylistSong.objects.create(playlist=playlist, song=song)
        result = {'result': 1, 'message': r'歌曲添加到歌单成功！', 'playlist_song_id': playlist_song.id}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def get_songs_in_favo(request):
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    if request.method == 'GET':
        user = User.objects.get(username=request.session['username'])
        favo_id = request.GET.get('favo_id')
        try:
            playlist = Playlist.objects.get(id=favo_id)
        except Playlist.DoesNotExist:
            result = {'result': 0, 'message': r'收藏夹不存在！'}
            return JsonResponse(result)
        if playlist.user.id != user.id:
            result = {'result': 0, 'message': r'不是你的歌单！'}
            return JsonResponse(result)
        playlist_songs = PlaylistSong.objects.filter(playlist=playlist).values('song_id', 'song__song_name',
                                                                               'song__singer')
        songs_data = [
            {
                'song_id': song['song_id'],
                'song_name': song['song__song_name'],
                'singer': song['song__singer']
            }
            for song in playlist_songs
        ]
        result = {'result': 1, 'message': r'获取收藏夹歌曲列表成功！', 'songs': songs_data}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def add_to_recent(request):
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        song_id = request.POST.get('song_id')

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            result = {'result': 0, 'message': r'歌曲不存在！'}
            return JsonResponse(result)

        # Check if the song is already in the recent play
        recent_play = RecentPlay.objects.filter(user=user, song=song).first()

        if recent_play:
            # Song is already in recent play, update the play date
            recent_play.play_date = timezone.now()
            recent_play.save()
            result = {'result': 1, 'message': r'歌曲已更新到最近播放！', 'recent_play_id': recent_play.id}
        else:
            # Song is not in recent play, create a new entry
            recent_play = RecentPlay.objects.create(user=user, song=song)
            result = {'result': 1, 'message': r'歌曲添加到最近播放成功！', 'recent_play_id': recent_play.id}

        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def post_max(request):
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'])
        max_recent_play_count = request.POST.get('max')

        try:
            # Convert the value from string to integer
            max_recent_play_count = int(max_recent_play_count)
            # Check if the value is valid
            if max_recent_play_count <= 0:
                raise ValueError("The value must be a positive integer")
        except ValueError as e:
            result = {'result': 0, 'message': r'最近播放最大数量必须是正整数！'}
            return JsonResponse(result)

        # Update the user's max recent play count
        user.recent_play_max = max_recent_play_count
        user.save()
        result = {'result': 1, 'message': r'设置最近播放最大数量成功！', 'recent_play_max': max_recent_play_count}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)


def get_record_list(request):
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    if request.method == 'GET':
        user = User.objects.get(username=request.session['username'])

        if user.recent_play_max == 0:
            result = {'result': 0, 'message': r'请设置最近播放的数量！'}
            return JsonResponse(result)

        recent_plays = RecentPlay.objects.filter(user=user).order_by('-play_date')
        song_count = recent_plays.aggregate(Count('id'))['id__count']
        max_play_count = user.recent_play_max

        if song_count <= max_play_count:
            recent_plays_data = recent_plays.values('song_id', 'song__song_name', 'song__singer')
        else:
            recent_plays_data = recent_plays[:max_play_count].values('song_id', 'song__song_name', 'song__singer')

        recent_plays_data_list = [
            {
                'song_id': recent_play['song_id'],
                'song_name': recent_play['song__song_name'],
                'singer': recent_play['song__singer']
            }
            for recent_play in recent_plays_data
        ]

        result = {'result': 1, 'message': r'获取最近播放列表成功！', 'recent_plays': recent_plays_data_list}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)

def get_uploaded_list(request):
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    if request.method == 'GET':
        username = request.session['username']
        user = User.objects.get(username=username)
        user_upload_songs = UserUploadSong.objects.filter(user=user).values('song_id', 'song__song_name', 'song__singer')

        songs_data = [
            {
                'song_id': song['song_id'],
                'song_name': song['song__song_name'],
                'singer': song['song__singer']
            }
            for song in user_upload_songs
        ]
        result = {'result': 1, 'message': r'获取用户上传的歌曲列表成功！', 'songs': songs_data}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)