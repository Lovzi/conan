from django.db import models
from django.utils.timezone import now

from conan import settings

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


class DoubtComment(models.Model):
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', related_name='doubt_comment_set',
                               on_delete=models.CASCADE)
    reply = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='回复', related_name='doubt_commented_set',
                              on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', verbose_name="上级评论", blank=True, on_delete=models.CASCADE)
    is_enable = models.BooleanField('是否显示', default=True, blank=False, null=False)
    doubt = models.ForeignKey('Doubt', verbose_name='问题', on_delete=models.CASCADE)
    star = models.IntegerField('点赞', default=0)
    is_doubt_comments = models.BooleanField(default=True)

    class Meta:
        db_table = 'doubt_comment'
        ordering = ['-created_time']
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)