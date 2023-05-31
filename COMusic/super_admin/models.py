from django.db import models

from comment.models import Comment
from music.models import Song, Playlist
from user.models import User


# Create your models here.


class Report(models.Model):  # 举报信息
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_sender')  # 发送方
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_receiver')  # 管理员，作为举报信息的接收者
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dic(self):
        result = {
            'report_id': self.id,
            'sender': self.sender.username,
            'time': self.created_at,
            'content': self.content,
        }
        return result
    class Meta:
        db_table = 'report'
