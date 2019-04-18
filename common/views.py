

# Create your views here.
import json

from django.views import View
from django.views.generic import TemplateView, ListView

from common.models import Tag
from common.models import Problem
from problem.views import ProblemListView
from utils.paginator import ProblemPaginator


class IndexView(TemplateView):
    template_name = 'index/index.html'
    def get_context_data(self, **kwargs):
        p = Tag(name='d')
        p.save()
        print(p.id)
        return super().get_context_data()


class SearchView(ListView):
    template_name = 'problem/problems.html'
    queryset = Problem.objects.all()
    context_object_name = 'problems'

    def get_queryset(self):
        params = self.request.GET.get('f')
        queryset = super().get_queryset().filter(title__icontains=params)
        return queryset


    def get_context_data(self, **kwargs):
        content = super(SearchView, self).get_context_data(**kwargs)
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


class ToolView(View):
    def get(self, request, *args, **kwargs):
        with open('../database/problems.json', 'r') as f:
            data = json.load(f)
        for single in data['data']['result']:
            fields = {
                'title': single['title'],
                'content': single['description'],
                'in_description': single['input_description'],
                'out_description': single['output_description'],
                'in_case': single['samples'][0]['input'],
                'out_case': single['samples'][0]['output'],
                'tip': single['hint'],
                'time_limited': single['time_limit'],
                'memory_limited': single['memory_limit'],
                'source': single['source']
                ''

            }
            Problem.objects.create()
