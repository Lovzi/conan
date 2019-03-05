from datetime import datetime

from django.db import models

# Create your models here.
from django.utils.timezone import now

from letcode import settings


class Problem(models.Model):
    title = models.CharField('题目', max_length=100, )
    content = models.TextField('描述')
    time_limited = models.IntegerField('时间限制', default=1000)
    memory_limited = models.IntegerField('空间限制', default=64)
    rank = models.IntegerField('等级')
    in_description = models.TextField('输入描述')
    out_description = models.TextField('输出描述')
    in_case = models.TextField('样例输入')
    out_case = models.TextField('样例输出')
    source = models.CharField('来源', max_length=50)
    tip = models.TextField('提示')


    class Meta:
        db_table = 'problem'
        verbose_name = '题库'
        verbose_name_plural = '题库'


class CommitRecord(models.Model):
    pid = models.IntegerField('题目编号')
    uid = models.IntegerField('用户编号')
    status = models.BooleanField('状态',default=False)
    result = models.CharField('结果', max_length=20, default="")
    cost_time = models.IntegerField('时间消耗', default=-1)
    cost_memory = models.IntegerField('内存消耗', default=-1)
    created_time = models.DateTimeField('提交时间', default=now)
    code = models.TextField('代码')
    language = models.CharField(max_length=15, default="N/A")

    class Meta:
        db_table = 'commit_record'
        verbose_name = '提交记录'
        verbose_name_plural = '提交记录'

    def serializer(self):
        return {
            'problem_id': self.pid,
            'user_id': self.uid,
            'status': self.status,
            'result': self.result,
            'cost_time': self.cost_time,
            'cost_memory': self.cost_memory,
            'created_time': datetime.strftime(self.created_time, '%Y-%m-%d %H-%M-%S'),
            'code': self.code
        }



class ProblemComment(models.Model):
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', related_name='problem_comment_set' , on_delete=models.CASCADE)
    reply = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='回复',null=True, blank=True, related_name='problem_commented_set', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', verbose_name="上级评论",related_name="children_comments", blank=True, null=True, on_delete=models.CASCADE)
    is_enable = models.BooleanField('是否显示', default=True)
    problem = models.ForeignKey('Problem', verbose_name='问题', on_delete=models.CASCADE)
    star = models.IntegerField('点赞', default=0)
    is_problem_comment = models.BooleanField(default=True)

    class Meta:
        db_table = 'problem_comment'
        ordering = ['-created_time']
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'

    def __str__(self):
        return self.body

    def serializer(self, field_name):
        return self.__dict__
