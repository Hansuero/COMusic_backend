from django.db import models
from user.models import User


# Create your models here.
class Song(models.Model):
    song_name = models.CharField('歌曲名', max_length=30)
    song_url = models.CharField('歌曲路径', max_length=128, default='')
    song_url_out = models.CharField('外部歌曲路径', max_length=128, default='')
    song_tag = models.CharField('歌曲标签', max_length=256, default='')
    song_cover_url = models.CharField('歌曲封面路径', max_length=128, default='')
    song_cover_url_out = models.CharField('外部歌曲封面路径', max_length=128, default='')
    singer = models.CharField('歌手名', max_length=30, default='佚名')
    lyric = models.TextField('歌词')

    def to_dic(self):
        result = {
            'song_id': self.id,
            'song_name': self.song_name,
            'song_cover_photo_url': self.song_cover_url_out,
            'singer': self.singer,

        }
        return result

    def to_simple_dic(self):
        result = {
            'song_id': self.id,
            'song_cover_url': self.song_cover_url_out,
        }
        return result

    class Meta:
        db_table = 'song'


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField('歌单名', max_length=30)
    is_shared = models.BooleanField('是否共享', default=False)
    playlist_tag = models.CharField('歌单标签', max_length=256, default='')
    playlist_cover_url = models.CharField('歌单封面路径', max_length=128, default='')	
    playlist_cover_url_out = models.CharField('外部歌单封面路径', max_length=128, default='')	
     
    def to_dic(self):
        result = {
            'playlist_id': self.id,
            'playlist_name': self.playlist_name,
            'owner_name': self.user.username,
            'playlist_tag': self.playlist_tag,
            'playlist_cover_photo_url': self.playlist_cover_url_out,
        }
        return result

    def to_simple_dic(self):
        result = {
            'playlist_id': self.id,
            'playlist_cover_url': self.playlist_cover_url_out,
        }
        return result

    class Meta:
        db_table = 'playlist'


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'playlist_song'


class UserUploadSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_upload_song'


class RecentPlay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    play_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recent_play'
