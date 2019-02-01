import random

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, TemplateView

from problem.views import ProblemDetailView


class RankView(ListView):
    pass


class PracticeView(TemplateView):
    pass


class RandomView(ProblemDetailView):
    def get_object(self, queryset=None):
        queryset_length = len(self.queryset)
        self.kwargs['id'] = random.randint(1, queryset_length)
        return super().get_object()
