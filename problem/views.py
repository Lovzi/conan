import math

from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView

from problem.models import Problem

class ProblemListView(ListView):
    template_name = 'problem/problems.html'
    context_object_name = 'problem_list'
    queryset = Problem.objects.all()
    PAGE_LIMITED = 50

    def __init__(self):
        self.page_index = None
        super().__init__()

    def get_queryset(self):
        try:
            page = int(self.request.GET.get('page', 1))
        except :
            pass
        offset = (page- 1) * self.PAGE_LIMITED
        return super().get_queryset()[offset:offset+self.PAGE_LIMITED]

    def get_context_data(self, **kwargs):
        content = super(ProblemListView, self).get_context_data(**kwargs)
        content['page_index'] = self.get_page_index_lst()
        return content

    def get_page_index_lst(self, ):
        page = int(self.request.GET.get('page', 1))
        if self.page_index is not None and (page > self.page_index[0] and page < self.page_index[-1]) :
            return self.page_index
        else:
            data_page_size = math.ceil(self.queryset.count() / self.PAGE_LIMITED)
            end_page = math.ceil(min(data_page_size, max(page + 3, 6)))
            begin_page = math.floor(max(page-3, 1))
            self.page_index = [i for i in range(begin_page, end_page+1)]
            return self.page_index


class ProblemDetailView(DetailView):
    template_name = 'problem/detail.html'
    context_object_name = 'problem'
    queryset = Problem.objects.all()
    pk_url_kwarg = 'id'




class AnswerView(CreateView):
    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data.get('code'))
        return HttpResponse('chenggon g ')