from django.db import models

# Create your models here.


class Score(models.Model):
    score = models.IntegerField(verbose_name='分数', default=0)
    accepted_num = models.IntegerField(verbose_name='通过数量', default=0)
    failed_num = models.IntegerField(verbose_name='失败数量', default=0)