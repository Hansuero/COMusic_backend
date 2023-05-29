from django.db import models

from comment.models import Comment
from music.models import Song, Playlist
from user.models import User


# Create your models here.


class Message(models.Model):  # 举报信息
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_sent')  # 发送方
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')  # 管理员，作为举报信息的接收者
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message'
