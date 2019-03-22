from django.contrib import admin

# Register your models here.

from contest.models import Contest, ContestGrade, ContestQuestion, ContestCommitRecord

admin.site.register([Contest, ContestQuestion, ContestGrade, ContestCommitRecord])