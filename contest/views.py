import datetime
import random
import time
import hashlib

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from django.core.mail import send_mail

from common.models import Contest, ContestStatus, Group, Problem, ContestGrade, User
from common.forms import *
from conan.settings import *

class ContestIndexView(TemplateView):
    template_name = 'contest/index.html'

    def is_apply(self, request):
        if request.user.group is not None:
            group_id = request.user.group.id
        else:
            return False
        if self.last_contest is not None \
                and self.last_contest.group.filter(id=group_id):
                return True
        return False

    def _format_contest_time(self):
        format_str = datetime.datetime.strftime(self.last_contest.start_time,
                                                '%Y-%m-%d %H:%M')
        format_str += " ~ " + datetime.datetime.strftime(self.last_contest.end_time,
                                                '%H:%M')
        return format_str

    def _get_duration(self, contest):
        duration = contest.end_time - contest.start_time
        hours = duration.seconds // 3600
        minutes = duration.seconds % 3600 // 60
        return {'hour': hours, 'minute': minutes}

    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self, request, *args, **kwargs):

        object_list = Contest.objects.all().order_by('start_time')
        if len(object_list):
            self.last_contest = object_list[len(object_list) - 1]
            self.ohter_contest = object_list[:len(object_list) - 1]
            for contest in self.ohter_contest:
                contest.duration = self._get_duration(contest)
            status = self.last_contest.status
            # 申请竞赛中
            if status == ContestStatus.CONTEST_APPLYING:
                # if self.is_apply(request):
                #     self.extra_context = {
                #         'ContestStatus': 5,
                #         'message': '等待比赛开始',
                #         'data': {
                #             'contest_info': {
                #                 'title': self.last_contest.title,
                #                 'time': self._format_contest_time()
                #             },
                #             'url': '/contest/%s/' %
                #         }
                #     }
                # else:
                self.extra_context = {
                    'ContestStatus': status,
                    'message': '参加这场竞赛',
                    'data': {
                        'contest_info': {
                            'title': self.last_contest.title,
                            'time': self._format_contest_time()
                        },
                        'url': '/contest/%s/detail/' % self.last_contest.id
                    }
                }
            # 申请竞赛结束
            elif status == ContestStatus.CONTEST_APPLY_END:
                if self.is_apply(request):
                    self.extra_context = {
                        'ContestStatus': "5",
                        'message': '等待比赛开始',
                        'data': {
                            'contest_info': {
                                'title': self.last_contest.title,
                                'time': self._format_contest_time()
                            },
                            'url': '/contest/%s/detail/' % self.last_contest.id
                        }
                    }

                else:
                    self.extra_context = {
                        'ContestStatus': status,
                        'message': '对不起，您错过了申请竞赛时间,可以进行模拟竞赛',
                        'virtualcontesturl': '/contest/virtual_contest/',
                        'data': {
                            'contest_info': {
                                'title': self.last_contest.title,
                                'time': self._format_contest_time()
                            },
                            'url': 'javascript:void(0);'
                        }

                    }
            elif status == ContestStatus.CONTEST_UNDERWAY and self.is_apply(request):
                # duration = self.last_contest.end_time - self.last_contest.start_time
                # hours = duration.seconds // 3600
                # minutes = duration.seconds % 3600 // 60
                self.extra_context = {
                    'ContestStatus': status,
                    'message': "正在进行%s" % self.last_contest.title,
                    'data': {
                            'contest_info': {
                                'title': self.last_contest.title,
                                'time': self._format_contest_time()
                            },
                            'url': '/contest/%s/' % self.last_contest.id
                    }
                }
            else:
                self.extra_context = {
                    'ContestStatus': status,
                    'message': "暂时没有竞赛",
                    'data': {
                        'contest_info': {
                            'title': "去进行虚拟竞赛吧",
                        },
                        'url': 'javascript:void(0);'
                    }
                }
        else:
            self.extra_context = {
                'ContestStatus': "1",
                'message': "暂时没有竞赛",
                'data': {
                    'contest_info': {
                        'title': "去进行虚拟竞赛吧",
                    },
                    'url': 'javascript:void(0);'
                }
            }
        self.extra_context['contests'] = self.ohter_contest
        return super().get(request, *args, **kwargs)


class GroupCreateView(TemplateView):
    template_name = 'contest/create-group.html'


class ContestView(TemplateView):
    template_name = 'contest/contest.html'

    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self, request, *args, **kwargs):
        if not request.user.is_captain:
            redirect('/contest/')
        contest_id = kwargs['contest_id']
        try:
            contest = Contest.objects.get(id=contest_id)
            problems = Problem.objects.filter(contest=contest)
            print(problems)
            #grades = Contest.objects.
            if not contest.group.filter(id=request.user.group.id):
                redirect('/contest/')
            self.extra_context={
                'contest': contest,
                'problems': problems
            }
        except:
            return Http404()
        return super().get(request, *args, **kwargs)


class Util:
    @staticmethod
    def send_email(request, msg='null'):
        hm = hashlib.md5((request.user.username+request.user.email).encode('utf8'))
        m = hm.hexdigest()
        try:
            send_mail(subject='验证邮箱',
                      message='激活队伍地址：http://%s/accounts/activate/?activate=%s&msg=%s' % (request.get_host(), m, msg),
                      from_email=EMAIL_FROM,
                      recipient_list=[request.user.email],
                      )  # fail_silently=False
            return True
        except:
            return False

    @staticmethod
    def send_apply(request, captain_email, captain_name):
        hm = hashlib.md5((captain_name + captain_email).encode('utf8'))
        m = hm.hexdigest()
        try:
            status = send_mail(subject='来自用户：%s的申请' % request.user.username,
                               message='同意点击该地址，不同意请忽略：http://%s/accounts/agree/?activate=%s&msg=%s' % (request.get_host(), m, request.user.username),
                               from_email=EMAIL_FROM,
                               recipient_list=[captain_email],
                               )   # fail_silently=False
            return True
        except:
            return False


# 申请加入竞赛 url：/contest/apply/
class ApplyContest(View):
    @method_decorator(login_required(login_url='/accounts/login/'))
    def post(self, request, *args, **kwargs):
        self.respon = {'message': '报名成功', "detail": "不要错过比赛哦~", 'data': '', 'code': 10000}
        if request.user.is_captain and request.user.group is not None:
            if not request.user.group.is_activate:
                self.respon['message'] = '您的队伍尚未激活'
                self.respon['detail'] = '我们将向您的邮箱发送激活信息，请保证您的邮箱是有效的哦\n'
                self.respon['code'] = 10008
                self.respon['is_valid_email'] = Util.send_email(request)
                print(request.user.email)
            else:
                contest_id = self.request.POST.get('contest_id')
                try:
                    contest = Contest.objects.get(pk=contest_id)
                except:
                    self.respon['detail'] = "对不起，没有这场竞赛"
                    self.respon['message'] = '报名失败'
                    self.respon['code'] = 10003
                    return JsonResponse(self.respon)
                contest.group.add(request.user.group)
                contest.save()
                print(contest.group.all())
        elif request.user.group is not None:
            self.respon['detail'] = "对不起，目前申请参加竞赛只允许队长申请"
            self.respon['message'] = '报名失败'
            self.respon['code'] = 10001
        else:
            self.respon['detail'] = '对不起您目前还未加入战队，是否创建队伍？'
            self.respon['message'] = '报名失败'
            self.respon['code'] = 10002

        return JsonResponse(self.respon)


class ContestCancel(View):
    def post(self, request, *args, **kwargs):
        self.respon = {'message': '未知错误！', 'code': -10009, "detail": "请稍后重试！"}
        try:
            contest_id = request.POST.get('contest_id')
            contest = Contest.objects.get(pk=contest_id)
            contest.group.remove(request.user.group)
            self.respon['detail'] = "您已经退出本次比赛"
            self.respon['message'] = '操作成功'
            self.respon['code'] = -10000
        except Exception as e:
            self.respon['detail'] = str(e)
        return JsonResponse(self.respon)


class ContestApplyCancel(View):
    @method_decorator(login_required(login_url='/accounts/login/'))
    def post(self, request, *args, **kwargs):
        self.respon = {'message': '未知错误！', 'code':-10003, "detail": "请稍后重试！"}
        if request.user.group is None:
            self.respon['detail'] = "您似乎并没有加入队伍"
            self.respon['message'] = '操作失败'
            self.respon['code'] = -10001
        else:
            contest_id = request.POST.get('contest_id')
            try:
                contest = Contest.objects.get(pk=contest_id)
            except Exception as e:
                self.respon['detail'] = "未知请求出错，请重试"
                self.respon['message'] = '操作失败'
                self.respon['code'] = -10009
                return JsonResponse(self.respon)
            try:
                contest.group.remove(request.user.group)
                self.respon['detail'] = "您已经取消本次报名"
                self.respon['message'] = '操作成功'
                self.respon['code'] = -10000
            except Exception as e:
                print(e)
                self.respon['detail'] = "您似乎并未加入此比赛，请重试"
                self.respon['message'] = '操作失败'
                self.respon['code'] = -10002
        return JsonResponse(self.respon)


# 创建战队 url：/contest/group/
class CreateGroup(View):

    @method_decorator(login_required(login_url='/accounts/login/'))
    def post(self, request, *args, **kwargs):
        print ('****************')
        self.respon = {'message': '未知错误！', 'code': 10003, "detail": "请稍后重试！"}
        try:
            if request.user.group is None:
                name = request.POST.get('name', '')
                if Group.objects.filter(name=name):
                    self.respon['message'] = '创建队伍失败'
                    self.respon['detail'] = "队伍名已存在！"
                    self.respon['code'] = 10008
                    return JsonResponse(self.respon)
                introduce = request.POST.get('introduce', '该队伍暂还没有介绍')
                captain = request.user.username
                group_obj = Group(name=name, introduce=introduce, captain=captain, people_num=1)
                if Util.send_email(request):
                    print(request.user.email)
                    group_obj.save()
                    request.user.is_captain = True
                    request.user.group = group_obj
                    request.user.save()
                    self.respon['message'] = '创建队伍成功！'
                    self.respon['detail'] = "为了保证后续队员加入，请先去邮箱激活您的队伍~"
                    self.respon['code'] = 10000
                else:
                    self.respon['message'] = '发送邮件失败了'
                    self.respon['detail'] = "您的邮箱似乎不对哦~"
                    self.respon['code'] = 10009
            else:
                self.respon['message'] = "您已经加入队伍！"
                self.respon['message'] = "可以进行报名了~"
                self.respon['code'] = 10004
        except Exception as e:
            print(self.respon, e)
        return JsonResponse(self.respon)



# 申请加入队伍 url：/contest/apply_group/?name=group_name
class ApplyAddGroup(View):

    @method_decorator(login_required(login_url='/accounts/login/'))
    def post(self, request, *args, **kwargs):
        respon = {'message': 'success', 'detail': '', 'code': 10000}
        group_name = request.POST.get('name', '')
        self.status = False
        try:
            group_obj = Group.objects.get(name=group_name)
        except:
            respon['message'] = "申请失败"
            respon['detail'] = '您输入的队伍不存在'
            respon['code'] = 10012
            return JsonResponse(respon)
        if group_name == '':
            respon['message'] = "申请失败"
            respon['detail'] = '您的输入不合法'
            respon['code'] = 10011
        elif request.user.group is not None:
            respon['message'] = "申请失败"
            respon['detail'] = '您已经有队伍了'
            respon['code'] = 10019
        else:
            for i in group_obj.users.all():
                if i.is_captain:
                    self.status = Util.send_apply(request, captain_email=i.email, captain_name=i.username)
                    break
            respon['message'] = "申请已被提交"
            respon['detail'] = '您的申请已通知该队伍队长，请耐心等待'
            respon['code'] = 10000
            # if not self.status:
            #     respon['message'] = '申请失败，请再次尝试'
            #     respon['code'] = 10013
            # else:
            #     respon['message'] = 'success'
            #     respon['code'] = 10000
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
    template_name = 'contest/problem-detail.html'
    context_object_name = 'problem'
    queryset = Problem.objects.all()
    pk_url_kwarg = 'problem_id'



class ContestPreviousView(ListView):
    template_name = 'contest/previous.html'
    queryset = Contest.objects.all()
    context_object_name = 'contests'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        return queryset

class ContestDetailView(TemplateView):
    template_name = 'contest/detail.html'

    def _get_start_time(self):
        duration = self.contest.start_time - datetime.datetime.now()
        day = duration.days
        second = duration.seconds
        hour = second // 3600
        minite = second % 3600 // 60
        second = second % 60
        return day, hour, minite, second

    def get(self, request, *args, **kwargs):
        contest_id = kwargs.get('contest_id')
        print(kwargs)
        print(self.kwargs)
        self.contest = Contest.objects.get(pk=contest_id)
        is_apply = False
        if request.user.is_authenticated:
            if request.user.group is None:
                is_apply = False
            else:
                try:
                    self.contest.group.get(pk=request.user.group.id)
                    is_apply = True
                except:
                    is_apply = False
        self.extra_context = {
            'contest': self.contest,
            'time': self._get_start_time(),
            'timestamp': time.mktime(self.contest.start_time.timetuple()),
            'is_apply': is_apply
        }
        return super().get(request, *args, **kwargs)



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

