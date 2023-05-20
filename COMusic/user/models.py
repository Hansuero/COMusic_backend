from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField('用户名', max_length=30)
    password = models.CharField('密码', max_length=32)
    email = models.EmailField()
    photo_url = models.CharField('用户头像路径', max_length=128, default='')
    bio = models.CharField('个人简介', max_length=256, default='')
    followers = models.ManyToManyField('self', through='Follow', related_name='following',
                                       symmetrical=False)
    is_admin = models.BooleanField('是否为管理员', default=False)

    class Meta:
        db_table = 'user'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
