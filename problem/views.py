import math

from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView

from problem.models import Problem
from utils.paginator import ProblemPaginator


class ProblemListView(ListView):
    template_name = 'problem/problems.html'
    context_object_name = 'problem_lst'
    queryset = Problem.objects.all()
    PAGE_LIMITED = 50

    def get_context_data(self, **kwargs):
        content = super(ProblemListView, self).get_context_data(**kwargs)
        try:
            current_page = int(self.request.GET.get('page', 1))
        except:
            current_page = 1
        paginator = ProblemPaginator(object_list=content.get('problem_lst', self.queryset),
                                     per_page=50,
                                     current_page=current_page)
        content['problem_lst'] = paginator.page(paginator.current_page)
        content['paginator'] = paginator
        content['current_page'] = paginator.current_page
        return content


class ProblemDetailView(DetailView):
    template_name = 'problem/detail.html'
    context_object_name = 'problem'
    queryset = Problem.objects.all()
    pk_url_kwarg = 'id'


class AnswerView(CreateView):
    def post(self, request, *args, **kwargs):
        data = request.POST
