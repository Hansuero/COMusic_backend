import json
import os

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from COMusic import settings
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

        playlist_tag = "未分类"
        if Playlist.objects.filter(user=user, playlist_name=playlist_name).exists():
            result = {'result': 1, 'message': r'收藏夹名字已存在！'}
            return JsonResponse(result)
        new_favo = Playlist.objects.create(user=user, playlist_name=playlist_name, playlist_tag=playlist_tag)
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


def set_shared(request):
    # 判断用户是否已经登录
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    # 判断是否是POST请求
    if request.method != 'POST':
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)

    # 从session中获取username
    username = request.session['username']

    # 从请求的POST数据中获取playlist_id
    playlist_id = request.POST.get('playlist_id', None)
    playlist_tag = request.POST.get('playlist_tag')  # 获取播放列表标签
    playlist_cover = request.FILES.get('playlist_cover')  # 获取封面文件
    if not playlist_id:
        result = {'result': 0, 'message': r'未提供playlist_id！'}
        return JsonResponse(result)

    try:
        # 查找对应的用户和播放列表
        user = User.objects.get(username=username)
        playlist = Playlist.objects.get(id=playlist_id, user=user)

        # 将播放列表的is_shared属性设置为True并保存
        playlist.is_shared = True
        playlist.save()
        if playlist_cover:  # 如果上传了封面文件
            _, ext = os.path.splitext(playlist_cover.name)
            playlist_cover_path = os.path.join(settings.BASE_DIR, 'playlist_cover', f'{playlist.id}_cover{ext}')
            playlist.playlist_cover_url = playlist_cover_path
            playlist.save()

            with open(playlist_cover_path, 'wb') as file:
                for chunk in playlist_cover.chunks():
                    file.write(chunk)
        else:
            playlist.playlist_cover_url = os.path.join(settings.BASE_DIR, 'playlist_cover', 'default.jpg')
            playlist.save()

        if playlist_tag:
            playlist.playlist_tag = playlist_tag
            playlist.save()

        result = {'result': 1, 'message': r'播放列表成功设置为共享！'}

    except User.DoesNotExist:
        result = {'result': 0, 'message': r'用户不存在！'}

    except Playlist.DoesNotExist:
        result = {'result': 0, 'message': r'播放列表不存在或不属于当前用户！'}

    return JsonResponse(result)


def unshare_songlist(request):
    # 判断用户是否已经登录
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    # 判断是否是POST请求
    if request.method != 'POST':
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)

    # 从session中获取username
    username = request.session['username']

    # 从请求的POST数据中获取playlist_id
    playlist_id = request.POST.get('songlist_id', None)

    if not playlist_id:
        result = {'result': 0, 'message': r'未提供playlist_id！'}
        return JsonResponse(result)

    try:
        # 查找对应的用户和播放列表
        user = User.objects.get(username=username)
        playlist = Playlist.objects.get(id=playlist_id, user=user)
        if not playlist.is_shared:
            result = {'result': 0, 'message': r'这不是歌单，无法取消分享！'}
            return  JsonResponse(result)
        # 将播放列表的is_shared属性设置为False并保存
        playlist.is_shared = False
        playlist.playlist_tag = "" # 清空播放列表标签
        playlist.playlist_cover_url = ""  # 清空封面
        playlist.save()

        result = {'result': 1, 'message': r'播放列表成功取消共享！'}

    except User.DoesNotExist:
        result = {'result': 0, 'message': r'用户不存在！'}

    except Playlist.DoesNotExist:
        result = {'result': 0, 'message': r'播放列表不存在或不属于当前用户！'}

    return JsonResponse(result)


def add_songs_to_favo(request):
    # 判断用户是否已经登录
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    # 判断是否是POST请求
    if request.method != 'POST':
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)

    # 从session中获取username
    username = request.session['username']
    user = User.objects.get(username=username)

    # 从请求的POST数据中获取song_ids和playlist_id
    song_ids_str = request.POST.get('songs_id')  # 获取 JSON 格式的 song_ids
    song_ids = json.loads(song_ids_str)
    playlist_id = request.POST.get('playlist_id')

    # 用来保存已成功添加的歌曲id
    added_songs = []

    try:
        # 获取播放列表
        playlist = Playlist.objects.get(id=playlist_id, user=user)
    except Playlist.DoesNotExist:
        result = {'result': 0, 'message': r'歌单不存在！'}
        return JsonResponse(result)

    for song_id in song_ids:
        try:
            # 获取歌曲
            song = Song.objects.get(id=song_id)

            # 将歌曲添加到播放列表
            playlist_song = PlaylistSong.objects.create(playlist=playlist, song=song)
            added_songs.append(playlist_song.id)
        except Song.DoesNotExist:
            continue  # 如果歌曲不存在，跳过并处理下一个歌曲

    result = {'result': 1, 'message': r'歌曲添加到歌单成功！', 'added_playlist_songs': added_songs}
    return JsonResponse(result)


def get_playlist(request):
    # 判断是否已经登录
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    # 判断是否是GET请求
    if request.method != 'GET':
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)

    # 从请求的GET数据中获取playlist_id
    playlist_id = request.GET.get('playlist_id', None)
    if not playlist_id:
        result = {'result': 0, 'message': r'未提供playlist_id！'}
        return JsonResponse(result)

    try:
        # 查找对应的播放列表
        playlist = Playlist.objects.get(id=playlist_id)

        # 查询歌单内的歌曲
        playlist_songs = PlaylistSong.objects.filter(playlist=playlist)
        song_list = []
        for item in playlist_songs:
            song_list.append({
                "song_id": item.song.id,
                "song_name": item.song.song_name
            })

        result = {
            'result': 1,
            'message': r'获取歌单信息成功！',
            'playlist_name': playlist.playlist_name,
            'playlist_creator': playlist.user.username,
            'playlist_tag': playlist.playlist_tag,
            'playlist_songs': song_list
        }

    except ObjectDoesNotExist:
        result = {'result': 0, 'message': r'播放列表不存在！'}

    return JsonResponse(result)

def get_song(request):
    # 判断是否已经登录
    if 'username' not in request.session:
        result = {'result': 0, 'message': r'尚未登录！'}
        return JsonResponse(result)

    # 判断是否是GET请求
    if request.method != 'GET':
        result = {'result': 0, 'message': r'请求方式错误！'}
        return JsonResponse(result)

    # 从请求的GET数据中获取song_id
    song_id = request.GET.get('song_id', None)
    if not song_id:
        result = {'result': 0, 'message': r'未提供song_id！'}
        return JsonResponse(result)

    try:
        # 查找对应的歌曲
        song = Song.objects.get(id=song_id)

        result = {
            'result': 1,
            'message': r'获取歌曲信息成功！',
            'song_name': song.song_name,
            'singer': song.singer,
            'song_cover_url': song.song_cover_url,
            'song_url': song.song_url,
            'lyric': song.lyric
        }

    except ObjectDoesNotExist:
        result = {'result': 0, 'message': r'歌曲不存在！'}

    return JsonResponse(result)

def cancel_favo(request):
    # 判断用户是否已经登录
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)

    # 判断是否是POST请求
    if request.method != 'POST':
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)

    # 从session中获取username
    username = request.session['username']
    user = User.objects.get(username=username)

    # 从请求的POST数据中获取playlist_id和song_id
    playlist_id = request.POST.get('playlist_id')
    song_id = request.POST.get('song_id')

    try:
        # 获取播放列表
        playlist = Playlist.objects.get(id=playlist_id, user=user)

        # 获取要取消收藏的歌曲
        song = Song.objects.get(id=song_id)

        # 删除歌曲与播放列表的关联关系
        playlist_song = PlaylistSong.objects.get(playlist=playlist, song=song)
        playlist_song.delete()

        result = {'result': 0, 'message': r'取消收藏成功！'}
        return JsonResponse(result)
    except Playlist.DoesNotExist:
        result = {'result': 3, 'message': r'歌单不存在！'}
        return JsonResponse(result)
    except Song.DoesNotExist:
        result = {'result': 4, 'message': r'歌曲不存在！'}
        return JsonResponse(result)
    except PlaylistSong.DoesNotExist:
        result = {'result': 5, 'message': r'歌曲未收藏！'}
        return JsonResponse(result)


def delete_list(request):
    # 判断是否已经登录
    if 'username' not in request.session:
        result = {'result': 2, 'message': r'尚未登录！'}
        return JsonResponse(result)

    # 判断是否是 DELETE 请求
    if request.method != 'DELETE':
        result = {'result': 1, 'message': r'请求方式错误！'}
        return JsonResponse(result)

    # 从请求的 DELETE 数据中获取 playlist_id
    playlist_id = request.DELETE.get('playlist_id', None)
    if not playlist_id:
        result = {'result': 3, 'message': r'未提供 playlist_id！'}
        return JsonResponse(result)

    try:
        # 查找要删除的播放列表
        playlist = Playlist.objects.get(id=playlist_id)

        # 删除 playlist_song 表中与该播放列表相关联的记录
        PlaylistSong.objects.filter(playlist=playlist).delete()

        # 删除 playlist 表中的该播放列表
        playlist.delete()

        result = {'result': 0, 'message': r'删除播放列表成功！'}

    except ObjectDoesNotExist:
        result = {'result': 4, 'message': r'播放列表不存在！'}

    return JsonResponse(result)