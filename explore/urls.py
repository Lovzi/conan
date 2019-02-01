import random
from django.urls import path

from explore import views

app_name = 'explore'
urlpatterns = [
    path(r'rank/', views.RankView.as_view()),
    path(r'practice/', views.PracticeView.as_view()),
    path(r'random/', views.RandomView.as_view()),
]