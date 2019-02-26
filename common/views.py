from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView

from problem.models import Problem


class IndexView(TemplateView):
    template_name = 'index/index.html'


class SearchView(ListView):
    template_name = 'problem/problems.html'
    queryset = Problem.objects.all()

    def get_queryset(self):
        params = self.kwargs
        queryset = super().get_queryset().filter(**params)
        return queryset