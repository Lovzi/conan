from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


# Create your views here.
from problem.models import Problem


class ProblemListView(ListAPIView):
    queryset = Problem.objects.all()



class ProblemDetailView(APIView):
    pass