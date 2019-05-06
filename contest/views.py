import random

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from common.models import Contest, ContestStatus, Group, Problem, ContestGrade, User
from common.forms import *

class ContestIndexView(TemplateView):
    template_name = 'contest/index.html'

    def is_apply(self, request):
        if isinstance(request.user, User) and self.last_contest.start_time >= now():
            group = request.user.group
            if group in self.last_contest.group.all():
                return True
        return False

    def get(self, request, *args, **kwargs):
        object_list = Contest.objects.all().order_by('start_time')
        if len(object_list):
            self.last_contest = object_list[len(object_list) - 1]
            status = self.last_contest.status
            # 申请竞赛中
            if status == ContestStatus.CONTEST_APPLYING:
                if self.is_apply(request):
                    self.extra_context = {
                        'ContestStatus': 5,
                        'message': '等待比赛开始'
                    }
                else:
                    self.extra_context = {
                        'ContestStatus': status,
                        'apply_url': '/contest/apply/'
                    }
            # 申请竞赛结束
            elif status == ContestStatus.CONTEST_APPLY_END:
                if self.is_apply(request):
                    self.extra_context = {
                        'ContestStatus': 5,
                        'message': '等待比赛开始'
                    }
                else:
                    self.extra_context = {
                        'ContestStatus': status,
                        'message': '对不起，您错过了申请竞赛时间,可以进行模拟竞赛',
                        'virtualcontesturl': '/contest/virtual_contest/',

                    }
            elif status == ContestStatus.CONTEST_UNDERWAY and self.is_apply(request):
                duration = self.last_contest.end_time - self.last_contest.start_time
                hours = duration.seconds // 3600
                minutes = duration.seconds % 3600 // 60
                self.extra_context = {
                    'ContestStatus': status,
                    'last_contest': self.last_contest,
                    'hours': hours,
                    'minutes': minutes,
                    'contesturl':'',
                }
            else:
                self.extra_context = {
                    'last_contest': None,
                }
        else:
            self.last_contest = None
            self.extra_context = {
                'last_contest': self.last_contest
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
            contest_obj = Contest.objects.all().order_by('-start_time')[0]
            contest_obj.group.add(request.user.group)
            contest_obj.save()
        elif request.user.is_captain is False and request.user.group is not None:
            self.respon['message'] = '对不起，目前申请参加竞赛只允许队长申请'
            self.respon['code'] = 10001
        elif request.user.group is not None:
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
        self.respon = {'message': '', 'code':10003}
        if form_verify.is_valid() and request.user.group is None:
            name = request.POST.get('name', '')
            introduce = request.POST.get('introduce', '该队伍暂还没有介绍')
            captain = request.user.username
            request.user.is_captain = True
            request.user.save()
            group_obj = Group(name=name, introduce=introduce, captain=captain, people_num=1)
            group_obj.save()
            request.user.group = group_obj
            request.user.save()
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


# 虚拟竞赛 url：/contest/virtual_contest/
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

            grade_obj_list = [i for i in ContestGrade.objects.filter(contest=random.choice(self.queryset)).all().order_by('-grade')]
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
        return super(VirtualContestView, self).get(request, *args, **kwargs)
        # return JsonResponse(self.extra_context)

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

