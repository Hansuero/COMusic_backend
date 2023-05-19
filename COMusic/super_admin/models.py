from django.db import models

from comment.models import Comment
from music.models import Song, Playlist
from user.models import User


# Create your models here.


class Report(models.Model):  # 举报信息
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_sent')  # 发送方
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')  # 管理员，作为举报信息的接收者
    song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True, null=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report'
