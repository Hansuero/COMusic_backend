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

    def to_simple_dic(self):
        return {
            "id": self.id,
            "username": self.username,
            "photo_url": self.photo_url,
        }

    def to_dic(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            'photo_url': self.photo_url,
            'bio': self.bio,
            "is_admin": self.is_admin,
        }

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
