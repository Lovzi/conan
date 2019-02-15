# from django.urls import path, include
#
from django.urls import path

from contest import views

app_name = 'contest'
urlpatterns = [
    path(r'', views.IndexView.as_view()),
    path(r'<path: contest_name>', views.ContestView.as_view())
]

