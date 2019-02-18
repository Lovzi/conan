from django.db import models
from django.utils.timezone import now

from letcode import settings

# Create your models here.

class Doubt(models.Model):
    title = models.CharField(verbose_name='标题', max_length=64)
    content = models.TextField('内容')
    created_time = models.DateTimeField('发表时间', default=now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    star = models.IntegerField()
    comments = models.IntegerField()

    class Meta:
        db_table = 'doubt'
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-created_time']




