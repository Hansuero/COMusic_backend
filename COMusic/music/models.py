from django.db import models
from user.models import User


# Create your models here.
class Song(models.Model):
    song_name = models.CharField('歌曲名', max_length=30)
    song_url = models.CharField('歌曲路径', max_length=128, default='')
    song_tag = models.CharField('歌曲标签', max_length=256, default='')

    class Meta:
        db_table = 'song'


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField('歌单名', max_length=30)
    is_shared = models.BooleanField('是否共享', default=False)

    class Meta:
        db_table = 'playlist'


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        db_table = 'playlist_song'
