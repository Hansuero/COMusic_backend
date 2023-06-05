from django.db import models
from user.models import User
from music.models import Song


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    content = models.CharField('评论内容', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dic(self):
        result = {
            'comment': self.content,
            'comment_id': self.id,
            'comment_user_id': self.user.id,
        }
        return result

    class Meta:
        db_table = 'comment'

