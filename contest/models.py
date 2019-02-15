from django.db import models

# Create your models here.
# from problem.models import Problem
#
#
# class Contest(models.Model):
#     start_date = models.DateField()
#     duration = models.TimeField()
#     contest_name = models.CharField(max_length=30)
#     is_official = models.BooleanField(default=False)
#     is_finish = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'contest'
#         verbose_name = '竞赛'
#         verbose_name_plural = '竞赛'
#
#
# class contest_grade():
#     user_id = models.IntegerField()
#     grade = models.IntegerField()
#     time_cost = models.TimeField()
#


# class ContestQuestion(Problem):
#     contest_id = models.ForeignKey('contest')
#     score = models.IntegerField()
#
#     class Meta:
#         db_table = 'contest_question'
#         verbose_name = '比赛内容'