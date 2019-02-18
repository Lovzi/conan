from django.db import models


class Catagory(models.Model):
    name = models.CharField(max_length=20)
