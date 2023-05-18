from django.db import models

from comment.models import Comment


# Create your models here.


class Report(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'report'

