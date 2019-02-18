from django.db import models

# Create your models here.
from django.template.defaulttags import now

from letcode import settings


class ProblemComment(models.Model):
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者')
    parent_comment = models.ForeignKey('self', verbose_name="上级评论", blank=True, null=True, on_delete=models.CASCADE)
    is_enable = models.BooleanField('是否显示', default=True, blank=False, null=False)
    problem = models.ForeignKey('Problem', verbose_name='问题', on_delete=models.CASCADE)
    star = models.IntegerField('点赞', default=0)

    class Meta:
        db_table = 'problem_comments'
        ordering = ['-created_time']
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class DoubtComment(models.Model):
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', verbose_name="上级评论", blank=True, null=True, on_delete=models.CASCADE)
    is_enable = models.BooleanField('是否显示', default=True, blank=False, null=False)
    doubt = models.ForeignKey('Doubt', verbose_name='问题', on_delete=models.CASCADE)
    star = models.IntegerField('点赞', default=0)
    is_doubt_comments = models.BooleanField(default=True)

    class Meta:
        db_table = 'problem_comments'
        ordering = ['-created_time']
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)