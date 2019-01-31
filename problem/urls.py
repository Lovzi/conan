from django.urls import path

from . import views

app_name = 'problem'
urlpatterns = [
    path(r'', views.ProblemListView.as_view(), name='problems_lst'),
    path(r'<int:id>', views.ProblemDetailView.as_view(), name='problems_detail'),
]

