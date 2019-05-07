import random
import time
import hashlib

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from django.core.mail import send_mail

from common.models import Contest, ContestStatus, Group, Problem, ContestGrade, User
from common.forms import *
from conan.settings import *

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


class GroupCreateView(TemplateView):
    template_name = 'contest/create-group.html'


class ContestView(TemplateView):
    template_name = 'contest/contest.html'


class Util:
    @staticmethod
    def send_email(request, msg=''):
        hm = hashlib.md5((request.user.username+request.user.email).encode('utf8'))
        m = hm.hexdigest()
        status = send_mail(subject='验证邮箱',
                           message='激活地址：http://%s/contest/activate/?activate=%s&msg=%s' % (request.get_host(), m, msg),
                           from_email=EMAIL_FROM,
                           recipient_list=[request.user.email],
                           fail_silently=False)
        return status

    @staticmethod
    def send_apply(request, captain_email, captain_name):
        hm = hashlib.md5((captain_name + captain_email).encode('utf8'))
        m = hm.hexdigest()
        status = send_mail(subject='来自用户：%s的申请' % request.user.username,
                           message='同意点击改地址否则可忽略：http://%s/contest/agree/?activate=%s&msg=%s' % (request.get_host(), m, request.user.username),
                           from_email=EMAIL_FROM,
                           recipient_list=[captain_email],
                           fail_silently=False)
        return status


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
    template_name = 'contest/create-group.html'
    @method_decorator(login_required(login_url='/accounts/login/'))
    def post(self, request, *args, **kwargs):
        form_verify = VerifyCreateGroup(request.POST)
        self.respon = {'message': '', 'code':10003}
        if request.user.is_active_email is False and form_verify.is_valid():
            self.respon['message'] = '您的账户邮箱未激活'
            self.respon['code'] = 10008
            request.user.email = request.POST.get('email', '')
            request.user.save()
            Util.send_email(request, msg=request.POST.get('name', ''))
        elif form_verify.is_valid() and request.user.group is None:
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


# 激活邮箱 url：/contest/activate
class ActivateEmail(View):
    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self,request, *args, **kwargs):
        hm = hashlib.md5()
        respon = {'message': 'success', 'data': '', 'code': 10000}
        hm.update((request.user.username + request.user.email).encode('utf8'))
        if request.GET.get('activate', '') == hm.hexdigest():
            request.user.is_active_email = True
            if request.GET.get('msg', '') != '':
                name = request.GET.get('msg', '')
                introduce = request.POST.get('introduce', '该队伍暂还没有介绍')
                captain = request.user.username
                request.user.is_captain = True
                group_obj = Group(name=name, introduce=introduce, captain=captain, people_num=1)
                group_obj.save()
                request.user.group = group_obj
                respon['message'] = '已激活并创建队伍成功'
                respon['data'] = {'group_name':request.GET.get('msg', '')}
                respon['code'] = 10000
            request.user.save()
            return JsonResponse(respon)
        respon['message'] = 'fail'
        respon['code'] = 10007
        return JsonResponse(respon)


# 申请加入队伍 url：/contest/apply_group/?name=group_name
class ApplyAddGroup(ListView):

    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self, request, *args, **kwargs):
        respon = {'message': 'success', 'data': '', 'code': 10000}
        group_name = request.GET.get('name', '')
        group_obj = Group.objects.get(name=group_name)
        self.status = ''
        if group_name == '':
            respon['message'] = '您的输入不合法'
            respon['code'] = 10011
        elif group_obj is None:
            respon['message'] = '您输入的队伍不存在'
            respon['code'] = 10012
        elif request.user.group is not None:
            respon['message'] = '您已经有队伍了'
            respon['code'] = 10019
        else:
            for i in group_obj.users.all():
                if i.is_captain:
                    self.status = Util.send_apply(request, captain_email=i.email, captain_name=i.username)
                    break
            if not self.status:
                respon['message'] = '申请失败，请再次尝试'
                respon['code'] = 10013
            else:
                respon['message'] = 'success'
                respon['code'] = 10000
        return JsonResponse(respon)


# 同意申请加入队伍 url：/contest/agree/?activate=''&msg=申请者名字
class Agree(View):

    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self, request, *args, **kwargs):
        respon = {'message': 'success', 'data': '', 'code': 10000}
        hm = hashlib.md5((request.user.username + request.user.email).encode('utf8'))
        if request.GET.get('activate', '') == hm.hexdigest():
            # msg 申请者名字
            apply_name = request.GET.get('msg', '')
            apply_obj = User.objects.get(username=apply_name)
            agree_obj = request.user
            apply_obj.group = agree_obj.group
            apply_obj.group.people_num += 1
            agree_obj.group.users.add(apply_obj)
            apply_obj.save()
            agree_obj.group.save()
        else:
            respon['message'] = 'fial'
            respon['code'] = 10015
        return JsonResponse(respon)


# 虚拟竞赛 url：/contest/virtual_contest/
class VirtualContestView(ListView):
    template_name = 'contest/contest.html'
    queryset = Contest.objects.all().order_by('-id')

    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self, request, *args, **kwargs):
        self.extra_context = {'message': 'success', 'data': {}, 'code':10000}
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


# 进入竞赛 url： /contest/start/
class StartContest(ListView):
    pass


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


class VirtualContestProblemView(ContestProblemView):
    pass


class VirtualContestProblemDetailView(ContestProblemDetailView):
    pass

