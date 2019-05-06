from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, TemplateView

from accounts.forms import RegisterForm, LoginForm
from common.models import User


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if redirect_to is None:
            redirect_to = '/'
        kwargs['redirect_to'] = redirect_to

        return super(LoginView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)

        if form.is_valid():
            print(self.redirect_field_name)
            redirect_to = self.request.GET.get(self.redirect_field_name)
            auth.login(self.request, form.get_user())
            return super(LoginView, self).form_valid(form)
        else:
            return self.render_to_response({
                'form': form
            })


    def get_success_url(self):

        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=[self.request.get_host()]):
            redirect_to = self.success_url
        return redirect_to


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save(False)
        user.save(True)
        url = reverse('accounts:login')
        return HttpResponseRedirect(url)


class LogoutView(RedirectView):
    url = '/'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class ProfileUpdateView(View):
    def post(self, request, *args, **kwargs):
        field = request.POST.get('field')
        data = request.POST.get('data')
        if field and data and field[0] and data[0]:
            params = {'id': request.user.id, field: data}
            user = User(**params)
            user.save(update_fields=[field])
            res = {
                'status': True,
                'data': data,
                'msg': "修改成功"
            }
        else:
            res = {
                'status': False,
                'data': None,
                'msg': "数据不能为空哦"
            }
        return JsonResponse(res)

    def get(self, request, *args, **kwargs):
        print(self.kwargs, kwargs)


