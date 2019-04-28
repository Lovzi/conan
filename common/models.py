from datetime import datetime
import time

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# Create your models here.
from conan import settings


class Group(models.Model):
    name = models.CharField(max_length=50)
    introduce = models.CharField(max_length=254, blank=True)
    date_joined = models.DateTimeField(default=now)

    class Meta:
        db_table = 'group'


class User(AbstractUser):
    # username = models.CharField(verbose_name='用户名',max_length=40, unique=True)
    # password = models.CharField(verbose_name='密码', max_length=40, default="12345678")
    mugshot = models.ImageField('头像',
                                upload_to='upload/mugshots',
                                default="/static/upload/mugshots/default.jpg")
    phone = models.CharField(verbose_name='手机号', max_length=12, blank=True)
    nickname = models.CharField(verbose_name='昵称', max_length=20, blank=True)
    department = models.CharField(verbose_name='所在学院', max_length=20, blank=True)
    sex = models.CharField(verbose_name='性别', max_length=2, blank=True)
    birthday = models.DateField(verbose_name='生日', blank=True, null=True)
    introduce = models.CharField(verbose_name='个人介绍', max_length=254, blank=True)
    blog = models.CharField(verbose_name='博客/github', max_length=20, blank=True)
    last_login = models.DateField(verbose_name='最近登录', default=now)
    skill = models.CharField(verbose_name='技能', max_length=100, blank=True)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    group = models.ForeignKey(Group, related_name="users", on_delete=models.CASCADE, null=True)
    permissions = models.IntegerField(default=0)

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'tag'


class ContestStatus:
    CONTEST_APPLYING = "-2"
    CONTEST_APPLY_END = "-1"
    CONTEST_UNDERWAY = "0"
    CONTEST_ENDED = "1"


class Contest(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250, default="")
    is_official = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name="created_contests", on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    created_time = models.DateTimeField(default=now)
    apply_end = models.DateTimeField()

    class Meta:
        db_table = 'contest'
        verbose_name = '竞赛'
        verbose_name_plural = '竞赛'

    @property
    def status(self):
        if self.apply_end > now():
            # 没有开始 返回1
            return ContestStatus.CONTEST_APPLYING
        elif self.apply_end < now() and self.start_time > now():
            return ContestStatus.CONTEST_APPLY_END
        elif self.end_time < now():
            # 已经结束 返回-1
            return ContestStatus.CONTEST_ENDED
        else:
            # 正在进行 返回0
            return ContestStatus.CONTEST_UNDERWAY



class ContestApply(models.Model):
    contest = models.ForeignKey('Contest', related_name='applies',on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='applies',on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contest_apply'
        verbose_name = '比赛报名表'
        verbose_name_plural = verbose_name


class ContestGrade(models.Model):
    contest = models.ForeignKey('Contest', related_name="grade", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="grade", on_delete=models.CASCADE)
    grade = models.IntegerField()
    time_cost = models.TimeField(default=time.strptime('00:00:00', "%H:%M:%S"))
    is_simulation = models.IntegerField('是否模拟', default=False)

    class Meta:
        db_table = 'contest_grade'
        verbose_name = '竞赛成绩'
        verbose_name_plural = verbose_name



class Problem(models.Model):
    title = models.CharField('题目', max_length=100)
    content = models.TextField('描述')
    time_limited = models.IntegerField('时间限制', default=1000)
    memory_limited = models.IntegerField('空间限制', default=64*1024)
    rank = models.IntegerField('等级')
    in_description = models.TextField('输入描述')
    out_description = models.TextField('输出描述')
    in_case = models.TextField('样例输入')
    out_case = models.TextField('样例输出')
    source = models.CharField('来源', max_length=254)
    tip = models.TextField('提示')
    visible = models.BooleanField('是否显示', default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey(Contest, null=True, related_name="problems", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="created_problems", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='problems')

    last_modify = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'problem'
        verbose_name = '题库'
        verbose_name_plural = '题库'


class AbstractCommitRecord(models.Model):
    problem = models.ForeignKey(Problem, verbose_name='题目编号', related_name="%(class)s", on_delete=models.CASCADE)
    status = models.BooleanField('状态',default=False)
    result = models.CharField('结果', max_length=20, default="")
    cost_time = models.IntegerField('时间消耗', default=-1)
    cost_memory = models.IntegerField('内存消耗', default=-1)
    created_time = models.DateTimeField('提交时间', default=now)
    code = models.TextField('代码')
    language = models.CharField(max_length=15, default="N/A")

    class Meta:
        abstract = True


class ContestCommitRecord(AbstractCommitRecord):
    contest = models.ForeignKey(Contest, verbose_name='比赛', related_name="commits", on_delete=models.CASCADE)
    is_simulation = models.IntegerField('是否模拟', default=False)
    group = models.ForeignKey(Group, verbose_name='队伍', related_name="commits", on_delete=models.CASCADE)

    class Meta:
        db_table = 'group_commit_record'
        verbose_name = '比赛提交记录'
        verbose_name_plural = '比赛提交记录'


class ProblemCommitRecord(AbstractCommitRecord):
    user = models.ForeignKey(User, verbose_name='用户', related_name="commits", on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_commit_record'
        verbose_name = '问题提交记录'
        verbose_name_plural = '问题提交记录'

    def serializer(self):
        return {
            'problem_id': self.problem.id,
            'user_id': self.user.id,
            'status': self.status,
            'result': self.result,
            'cost_time': self.cost_time,
            'cost_memory': self.cost_memory,
            'created_time': datetime.strftime(self.created_time, '%Y-%m-%d %H-%M-%S'),
            'code': self.code
        }


class AbstractComment(models.Model):
    content = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', related_name="%(class)s",
                               on_delete=models.CASCADE)
    reply = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='回复',
                              related_name='%(class)s_replied', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', verbose_name="上级评论", related_name="children_comments", on_delete=models.CASCADE)
    visible = models.BooleanField('是否可见', default=True)
    star = models.IntegerField('点赞', default=0)
    is_private =models.BooleanField('是否私有', default=False)
    is_parent_comment = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ProblemComment(AbstractComment):
    problem = models.ForeignKey(Problem, verbose_name='问题', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        db_table = 'problem_comment'
        ordering = ['-created_time']
        verbose_name = "问题评论"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'

    def __str__(self):
        return self.content

    def serializer(self, field_name):
        return self.__dict__


class Doubt(models.Model):
    title = models.CharField(verbose_name='标题', max_length=64)
    content = models.TextField('内容')
    created_time = models.DateTimeField('发表时间', default=now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者',
                               related_name="doubts", on_delete=models.CASCADE)
    star = models.BigIntegerField()
    tags = models.ManyToManyField(Tag, related_name='doubts')

    class Meta:
        db_table = 'doubt'
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-created_time']


class DoubtComment(AbstractComment):
    doubt = models.ForeignKey(Doubt, related_name='comments', verbose_name='帖子', on_delete=models.CASCADE)

    class Meta:
        db_table = 'doubt_comment'
        ordering = ['-created_time']
        verbose_name = "帖子评论"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)