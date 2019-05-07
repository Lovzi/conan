# from django.urls import path, include
#
from django.urls import path


from contest import views

app_name = 'contest'
urlpatterns = [
    path(r'', views.ContestIndexView.as_view()),
    path(r'virtual_contest/', views.VirtualContestView.as_view()),
    path(r'previous/', views.ContestPreviousView.as_view()),
    path(r'apply/', views.ApplyContest.as_view(), name='apply'),
    path(r'group/', views.CreateGroup.as_view()),
    # path(r'groups/', views.GroupCreateView.as_view()),
    path(r'activate/',views.ActivateEmail.as_view()),
    path(r'apply_group/', views.ApplyAddGroup.as_view()),
    path(r'agree/', views.Agree.as_view()),
    path(r'start/', views.StartContest.as_view()),
    #path(r'<path:contest_name>/detail/', views.ContestDetailView.as_view()),
    # path(r'virtual_contest/random/', views.VirtualRandomView.as_view()),
    path(r'<str:contest_name>/', views.ContestView.as_view()),
    path(r'<str:contest_name>/detail/', views.ContestDetailView.as_view()),
    path(r'<str:contest_name>/problems/', views.ContestView.as_view()),
    # path(r'<str:contest_name>/problems/<str: problem_name>/',
    #      views.ContestProblemDetailView.as_view()),
    # path(r'virtual_contest/<str:contest_name>/', views.VirtualContestView.as_view()),
    # path(r'virtual_contest/<str:contest_name>/problems/',
    #      views.VirtualContestProblemView.as_view()),
    # path(r'virtual_contest/<str:contest_name>/problems/<str: problem_name>/',
    #      views.VirtualContestProblemDetailView.as_view()),
]

