from django.contrib import admin
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path(r'login/', views.LoginView.as_view(), name='login'),
    path(r'register/', views.RegisterView.as_view(), name='register'),
    path(r'logout/', views.LogoutView.as_view(), name='logout'),
    path(r'profile/', views.ProfileView.as_view(), name='profile'),
    path(r'profile/modules/', views.ProfileLoadView.as_view()),
    path(r'profile/<str:field>/', views.ProfileUpdateView.as_view()),
    path(r'activate/',views.ActivateEmail.as_view()),
]
