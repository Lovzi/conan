from django.urls import path

from . import views

urlpatterns= [
    path(r'problems/', views.ProblemListView.as_view, name='problems'),
    path(r'problems/<int:problem_id>', views.ProblemDetailView.as_view, name='problems_detail')
]

