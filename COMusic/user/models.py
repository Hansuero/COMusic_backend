from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField('用户名', max_length=30)
    password = models.CharField('密码', max_length=32)
    email = models.EmailField()
    photo_url = models.CharField('用户头像路径', max_length=128, default='')
    bio = models.CharField('个人简介', max_length=256, default='')

    class Meta:
        db_table = 'user'
