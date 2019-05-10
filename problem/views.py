import json
from datetime import datetime

import requests

from django.http import HttpResponseBadRequest, JsonResponse, QueryDict, HttpResponse
from django.template import loader
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from common.models import User
from common.models import Problem, ProblemComment, ProblemCommitRecord
from utils.paginator import ProblemPaginator


class ProblemListView(ListView):
    template_name = 'problem/problems.html'
    context_object_name = 'problems'
    queryset = Problem.objects.all()
    PAGE_LIMITED = 50

    def get_context_data(self, **kwargs):
        content = super(ProblemListView, self).get_context_data(**kwargs)
        try:
            current_page = int(self.request.GET.get('page', 1))
        except:
            current_page = 1
        paginator = ProblemPaginator(object_list=content.get('problems', self.queryset),
                                     per_page=50,
                                     current_page=current_page)
        content['problems'] = paginator.page(paginator.current_page)
        for problem in content['problems']:
            commit_num = ProblemCommitRecord.objects.filter(problem=problem).count()
            if commit_num:
                ac_num = ProblemCommitRecord.objects.filter(problem=problem, result="Accepted").count()
                problem.ac = float('%.2f' % (ac_num / commit_num * 100))
            else:
                problem.ac = 0
        content['paginator'] = paginator
        content['current_page'] = paginator.current_page
        return content


class ProblemDetailView(DetailView):
    template_name = 'problem/detail.html'
    context_object_name = 'problem'
    queryset = Problem.objects.all()
    pk_url_kwarg = 'id'


class AnswerView(View):
    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        problem_id = self.request.POST.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        language = self.kwargs.get('language')
        commit = ProblemCommitRecord(code=code,problem=problem_obj, user=request.user, language=language)
        commit.save()
        serialzer_data = {
            'code': code,
            'problem_id': commit.problem.id,
            'user_id': commit.user.id,
            'solution_id': commit.id,
            'created_time': datetime.strftime(commit.created_time, '%Y-%m-%d %H-%M-%S'),
            'time_limited': problem_obj.time_limited,
            'memory_limited': 32768
        }
        url = "http://39.96.194.42:5000/%s/" % self.kwargs['language']
        data = json.dumps(serialzer_data)

        res = requests.post(url=url, data=data, headers={'Content-Type': 'application/json'})
        print(res.content)
        data = json.loads(res.content)
        commit.__dict__.update(data)
        commit.save()
        return JsonResponse(data)


class ProblemCommitRecordView(ListView):
    template_name = 'problem/commit_record.html'
    context_object_name = 'records'
    queryset = ProblemCommitRecord.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        problem = Problem(id=self.kwargs.get('id'))
        return queryset.filter(problem=problem).order_by('-created_time').all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        template_text = loader.render_to_string(self.template_name, context=context, request=request)
        data = {'code': 0, 'content': template_text}
        return JsonResponse(data)

class ProblemCommentView(ListView):
    template_name = 'problem/comments.html'
    context_object_name = 'comments'
    queryset = ProblemComment.objects.all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        template_text = loader.render_to_string(self.template_name, context=context, request=request)
        data = {'code': 0, 'content': template_text}
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        comment_body = request.POST.get('comment', "")
        if not comment_body:
            return HttpResponseBadRequest('评论不能为空')
        comment = ProblemComment()
        comment.content = comment_body
        comment.problem = Problem(id=self.request.POST.get('problem_id'))
        comment.author = self.request.user
        print(request.POST.get('parent_comment_id'))
        if request.POST.get('parent_comment_id') and request.POST.get('replied_id'):
            reply = User(id=request.POST.get('replied_id'))
            comment.reply = reply
            comment.parent_comment = ProblemComment(id=request.POST.get('parent_comment_id'))
            comment.is_parent_comment = False
        comment.save()
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        template_text = loader.render_to_string(self.template_name, context=context, request=request)
        data = {'code': 0, 'content': template_text}
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        # try:
        put_dict= QueryDict(self.request.body)
        comment_id = put_dict.get('id')
        print(type(comment_id), comment_id)
        comment = self.queryset.get(id=comment_id)
        comment.star += 1
        comment.save()
        data = {'code': 0, 'content': comment.star}
        # except Exception as e:
        #     print(e)
        #     data = {'code': -1, 'content': '异常'}
        #     return JsonResponse(data)
        return JsonResponse(data)

    def get_queryset(self):
        self.problem = Problem(id=self.kwargs.get('id'))
        return super().get_queryset().filter(
            problem=self.problem, is_parent_comment=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data()
        content['problem_id'] = self.kwargs.get('id') or self.problem.id
        return content


class SolutionView(TemplateView):
    template_name = 'problem/solution.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        template_text = loader.render_to_string(self.template_name, context=context, request=request)
        data = {'code': 0, 'content': template_text}
        return JsonResponse(data)
