from django.contrib import admin
from django.urls import path
from common import views

app_name = 'common'
urlpatterns = [
    path('', views.IndexView.as_view()),
    path('search/', views.SearchView.as_view()),
    #path('tool/', views.ToolView.as_view())
]
