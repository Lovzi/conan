from django.shortcuts import render, render_to_response, HttpResponse
from django.views import View
# Create your views here.


class LoginView(View):
    def get(self, request):
        return HttpResponse('get')

    def post(self, request):
        return HttpResponse('post')



