from django.views.generic import ListView, DetailView

from problem.models import Problem

class ProblemListView(ListView):
    template_name = 'problem/problems.html'
    context_object_name = 'problem_list'
    queryset = Problem.objects.all()


class ProblemDetailView(DetailView):
    template_name = 'problem/detail.html'
    context_object_name = 'problem'
    model = Problem
    pk_url_kwarg = 'id'


