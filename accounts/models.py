from django.db import models
# Create your models here.

class User(models.Model):
    username = models.CharField(verbose_name='用户名',max_length=40, unique=True, null=False)
    password = models.CharField(verbose_name='密码', max_length=40)
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(verbose_name='手机号', max_length=12, default="")
    score = models.IntegerField(verbose_name='分数', default=0)
    accepted_num = models.IntegerField(verbose_name='通过数量', default=0)
    failed_num = models.IntegerField(verbose_name='失败数量', default=0)
    nickname = models.CharField(verbose_name='姓名', max_length=20, default=" ")
    department = models.CharField(verbose_name='所在学院', max_length=20, default="")
    sex = models.CharField(verbose_name='性别',max_length=2)
    birthday = models.DateField(verbose_name='生日')
    introduce = models.CharField(verbose_name='个人介绍', max_length=64, default="")
    blog = models.CharField(verbose_name='博客/github', max_length=20, default="")
    last_login = models.DateField(verbose_name='最近登录',)
    skill = models.CharField(verbose_name='技能', max_length=100)
    is_active = models.BooleanField(verbose_name='状态', default=True)

    class Meta:
        pass

