from django.urls import path, include

app_name = 'contest'
urlpatterns = [
    path(r'', include('contest.urls', namespace='contest')),

]

