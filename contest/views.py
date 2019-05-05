import random

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from common.models import Contest, ContestStatus, Group, Problem, ContestGrade
from common.forms import *

class ContestIndexView(TemplateView):
    template_name = 'contest/index.html'

    def get(self, request, *args, **kwargs):
        object_list = Contest.objects.all().order_by('start_time')
        if len(object_list):
            last_contest = object_list[len(object_list) - 1]
            status = last_contest.status
            # 申请竞赛中
            if status == ContestStatus.CONTEST_APPLYING:
                self.extra_context = {
                    'apply_url' : ''
                }
                pass
            elif status == ContestStatus.CONTEST_APPLY_END:
                pass
            elif status == ContestStatus.CONTEST_UNDERWAY:
                duration = last_contest.end_time - last_contest.start_time
                hours = duration.seconds // 3600
                minutes = duration.seconds % 3600 // 60
                self.extra_context = {
                    'last_contest': last_contest,
                    'hours': hours,
                    'minutes': minutes
                }
            else:
                self.extra_context = {
                    'last_contest': None,
                }
        else:
            last_contest = None
            self.extra_context = {
                'last_contest': last_contest
            }
        return super().get(request, *args, **kwargs)

class ContestView(TemplateView):
    template_name = 'contest/contest.html'


# 申请加入竞赛 url：/contest/apply/
class ApplyContest(View):
    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self, request, *args, **kwargs):
        self.respon = {'message': '申请竞赛成功', 'data': '', 'code': 10000}
        if request.user.is_captain:
            request.user.group.is_apply = True
            request.user.group.save()
        elif request.user.is_captain == False and request.user.group != None:
            self.respon['message'] = '对不起，目前申请参加竞赛只允许队长申请'
            self.respon['code'] = 10001
        elif request.user.group == None:
            self.respon['message'] = '对不起您目前还未加入战队，该比赛只能战队参加'
            self.respon['code'] = 10002
        else:
            pass
        return JsonResponse(self.respon)


# 创建战队 url：/contest/group/
class CreateGroup(ListView):
    # template_name = '/contest/creategroup.html'
    @method_decorator(login_required(login_url='/accounts/login/'))
    def post(self, request, *args, **kwargs):
        form_verify = VerifyCreateGroup(request.POST)
        self.respon = {'message':'', 'code':10003}
        if form_verify.is_valid():
            Group.name = request.POST.get('name', '')
            Group.introduce = request.POST.get('introduce', '该队伍暂还没有介绍')
            Group.captain = request.user.username
            Group.save()
            self.respon['message'] = '创建队伍成功'
            self.respon['code'] = 10000
        else:
            self.respon['message'] = form_verify.errors
            self.respon['code'] = 10004
        return JsonResponse(self.respon)




class ContestProblemView(ListView):
    pass


class ContestProblemDetailView(DetailView):
    pass


class ContestPreviousView(ListView):
    template_name = 'contest/previous.html'
    queryset = Contest.objects.all()
    context_object_name = 'contests'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        return queryset

class ContestDetailView(TemplateView):
    template_name = 'contest/detail.html'


class VirtualRandomView(View):
    def get(self, request, *args, **kwargs):
        obj = random.choice(Contest.objects.all())
        data = {
            'status': True,
            'contestName': obj.contest_name
        }
        return JsonResponse(data)


class VirtualContestView(ListView):
    template_name = 'contest/contest.html'
    queryset = Contest.objects.all().order_by('-id')
    @method_decorator(login_required(login_url='/accounts/login/'))

    def get(self, request, *args, **kwargs):
        self.extra_context = {'message': 'success', 'data': {}, 'code':'10000'}
        temp = []
        try:
            for i in self.get_queryset():
                temp.append({'title': i.title, 'content': i.content, 'time_limited': i.time_limited,
                             'memory_limited': i.memory_limited, 'rank': i.rank, 'in_description': i.in_description,
                             'out_description':i.out_description, 'in_case': i.in_case, 'out_case': i.out_case,
                             'source': i.source, 'tip': i.tip, 'visible': i.visible, 'created_time': i.created_time,
                             'contest': '模拟竞赛',  'tags': [obj.name for obj in i.tags.all()],
                             'last_modify': i.last_modify,'created_by': i.created_by.username})
                # print(temp[0])

            # 获取模拟竞赛题目等信息
            self.extra_context['data']['problem'] = temp

            grade_obj_list = [i for i in ContestGrade.objects.filter(contest=self.queryset[0]).all().order_by('-grade')]
            print(grade_obj_list)
            group_list = []
            for i in grade_obj_list[:15]:
                captain_touxiang = ''
                for user_obj in i.group.users.all():
                    if user_obj.is_captain:
                        captain_touxiang = user_obj.mugshot
                group_list.append({'name': i.group.name, 'introduce': i.group.introduce, 'captain': i.group.captain,
                                   'image': '/static/'+str(captain_touxiang), 'grade': i.grade, 'time_cost': i.time_cost})
            # 获取竞赛组排名，取前面十五个
            self.extra_context['data']['conan_ranking'] = group_list

        except Exception as e:
            self.extra_context['message'] = str(e)
            self.extra_context['data'] = ''
            self.extra_context['code'] = 10005
        # return super(VirtualContestView, self).get(request, *args, **kwargs)
        return JsonResponse(self.extra_context)



    def get_queryset(self):
        if self.queryset:
            new_contest_problem = Problem.objects.filter(contest=self.queryset[0]).all()
            return new_contest_problem[:4]
        else:
            return None

class VirtualContestProblemView(ContestProblemView):
    pass


class VirtualContestProblemDetailView(ContestProblemDetailView):
    pass

