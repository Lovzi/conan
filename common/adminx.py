#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 15:40
# @Author  : 徐纪茂
# @File    : adminx.py
# @Software: PyCharm
# @Email   : jimaoxu@163.com
import xadmin
from .models import *
class GroupXadmin(object):
    list_display = ['name', 'introduce','date_joined']

# class UserXadmin(object):
#     list_display = ['username','password','mugshot', 'phone','introduce']

class ContestXadmin:
    list_display = ['title', 'description']

class ContestApplyXadmin:
    list_display = ['contest','group']

class ContestGradeXadmin:
    list_display = ['contest', 'grade']

class ProblemXadmin:
    list_display = ['title', 'content', 'rank']

class ContestCommitRecordXadmin:
    pass

class ProblemCommitRecordXadmin:
    pass

class AbstractCommentXadmin:
    pass

class ProblemCommentXadmin:
    pass

class DoubtXadmin:
    pass

class DoubtCommentXadmin:
    pass

xadmin.site.register(Group, GroupXadmin)
xadmin.site.register(Contest, ContestXadmin)
xadmin.site.register(ContestApply, ContestApplyXadmin)
xadmin.site.register(ContestGrade, ContestGradeXadmin)
xadmin.site.register(Problem, ProblemXadmin)
xadmin.site.register(ContestCommitRecord,ContestCommitRecordXadmin)
xadmin.site.register(ProblemCommitRecord,ProblemCommitRecordXadmin)
xadmin.site.register(AbstractComment,AbstractCommentXadmin)
xadmin.site.register(ProblemComment,ProblemCommentXadmin)
xadmin.site.register(Doubt,DoubtXadmin)
xadmin.site.register(DoubtComment,DoubtCommentXadmin)

