from django.urls import path

from . import views

app_name = 'problem'
urlpatterns = [
    path(r'', views.ProblemListView.as_view(), name='problems_lst'),
    path(r'<int:id>', views.ProblemDetailView.as_view(), name='problems_detail'),
    path(r'answer/<path:language>', views.AnswerView.as_view(), name='answer'),
    path(r'<int:id>/comments/', views.ProblemCommentView.as_view()),
    #path(r'<int:id>/comments/star/')
]

