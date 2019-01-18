from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import User
from .serializers import UserSerialzer
from django.views import View


# Create your views here.


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    @csrf_exempt
    def post(self, request):
        return HttpResponse('post')


class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    @csrf_exempt
    def post(self, request):
        return HttpResponse('post')


