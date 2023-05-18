from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField('用户名', max_length=30)
    password = models.CharField('密码', max_length=32)
    email = models.EmailField()
    photo = models.FileField('用户头像', upload_to='')
    photo_url = models.CharField('用户头像路径', max_length=128, default='')
    bio = models.CharField('个人简介', max_length=256, default='')

    class Meta:
        db_table = 'user'
