#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 15:24
# @File    : forms.py
# @Software: PyCharm
from django import forms


class VerifyCreateGroup(forms.Form):
    name = forms.CharField(min_length=2,max_length=50)
    introduce = forms.CharField(max_length=254)

# class ActivateEmail(forms.Form):
#     captcha = captchaField()