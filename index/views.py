from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index/index.html'
