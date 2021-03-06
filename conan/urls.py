"""conan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from accounts import views
#import xadmin
#xadmin.autodiscover()

#from xadmin.plugins import xversion
#xversion.register_models()
import xadmin
urlpatterns = [
    path(r'', include('common.urls', namespace='common')),
    path(r'xadmin/', xadmin.site.urls),
    path(r'accounts/', include('accounts.urls', namespace='accounts')),
    path(r'problems/', include('problem.urls', namespace='problems')),
    path(r'contest/', include('contest.urls', namespace='contest')),
    path(r'explore/', include('explore.urls', namespace='explore')),
    path(r'discuss/', include('discuss.urls', namespace='discuss'))
]

