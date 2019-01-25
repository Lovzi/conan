from django.db import models

# Create your models here.

class problem(models.Model):
    title = models.CharField('题目', max_length=100, )
    content = models.TextField('描述')
    time_limited = models.IntegerField('时间限制', default=1000)
    memory_limited = models.IntegerField('空间限制', default=64)
    rank = models.IntegerField('等级')
    in_description = models.TextField('输入描述')
    out_description = models.TextField('输出描述')
    in_case =  models.TextField('样例输入')
    out_case = models.TextField('样例输出')
    source = models.CharField('来源', max_length=50)

    class Meta:
        db_table = 'problem'
        verbose_name = '题库'
        verbose_name_plural = '题库'


class CommitRecord(models.Model):
    pid = models.IntegerField()

    uid = models.IntegerField()

    status = models.BooleanField()

    code = models.TextField()



