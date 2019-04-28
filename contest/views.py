import random

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from common.models import Contest, ContestStatus


class ContestIndexView(TemplateView):
    template_name = 'contest/index.html'

    def get(self, request, *args, **kwargs):
        object_list = Contest.objects.all().order_by('start_time')
        if len(object_list):
            last_contest = object_list[-1]
            status = last_contest.status
            if status == ContestStatus.CONTEST_APPLYING:
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


class VirtualRandomView(View):
    def get(self, request, *args, **kwargs):
        obj = random.choice(Contest.objects.all())
        data = {
            'status': True,
            'contestName': obj.contest_name
        }
        return JsonResponse(data)


class VirtualContestView(ContestView):
    pass


class VirtualContestProblemView(ContestProblemView):
    pass


class VirtualContestProblemDetailView(ContestProblemDetailView):
    pass

