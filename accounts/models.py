from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
# Create your models here.

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
    introduce = models.CharField(verbose_name='个人介绍', max_length=64, blank=True)
    blog = models.CharField(verbose_name='博客/github', max_length=20, blank=True)
    last_login = models.DateField(verbose_name='最近登录', default=now)
    skill = models.CharField(verbose_name='技能', max_length=100, blank=True)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    is_group = models.BooleanField('是否队伍',default=False)

    class Meta:
        db_table = 'user'
        unique_together = ('username', 'is_group')
        verbose_name = '用户'
        verbose_name_plural = '用户'


