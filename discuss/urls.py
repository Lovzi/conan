from django.urls import path

from discuss import views

app_name = 'discuss'
urlpatterns = [
    path('', views.DoubtListView.as_view())
]