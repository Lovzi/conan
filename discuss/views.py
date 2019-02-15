from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView


class DoubtDetailView(DetailView):
    template_name = 'discuss/detail.html'


class DoubtListView(TemplateView):
    template_name = 'discuss/doubt.html'