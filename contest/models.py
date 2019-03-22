import time

from django.db import models
from django.utils.timezone import now

from letcode import settings
from problem.models import Problem, CommitRecord
from accounts.models import User


class Contest(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    contest_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, default="")
    is_official = models.BooleanField(default=False)
    is_finish = models.BooleanField(default=False)

    class Meta:
        db_table = 'contest'
        verbose_name = '竞赛'
        verbose_name_plural = '竞赛'


class ContestProposer(models.Model):
    contest = models.ForeignKey('Contest', related_name='proposer',on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contests',on_delete=models.CASCADE)

    class Meta:
        db_table = 'contest_proposer'
        verbose_name = '比赛报名表'
        verbose_name_plural = verbose_name



class ContestGrade(models.Model):
    contest_id = models.ForeignKey('Contest', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.IntegerField()
    time_cost = models.TimeField(default=time.strptime('00:00:00', "%H:%M:%S"))
    is_simulation = models.IntegerField('是否模拟', default=False)

    class Meta:
        db_table = 'contest_grade'
        verbose_name = '竞赛成绩'
        verbose_name_plural = verbose_name



class ContestQuestion(Problem):
    contest_id = models.ForeignKey('contest', on_delete=models.CASCADE)
    value = models.IntegerField('题目分值', default=10)

    class Meta:
        db_table = 'contest_question'
        verbose_name = '竞赛题目'
        verbose_name_plural = '竞赛题目'


class ContestCommitRecord(CommitRecord):
    cid = models.IntegerField('比赛编号')
    is_simulation = models.IntegerField('是否模拟', default=False)

    class Meta:
        db_table = 'contest_commit_record'
        verbose_name = '竞赛提交记录'
        verbose_name_plural = verbose_name


