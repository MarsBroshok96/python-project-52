from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

MSG_SUCCESS_LOGIN = "You are logged in"
MSG_SUCCESS_LOGOUT = "You are logged out"


class HomeView(TemplateView):
    template_name = "index.html"


class UserLoginView(SuccessMessageMixin, LoginView):
    next_page = 'homepage'
    success_message = MSG_SUCCESS_LOGIN


class UserLogoutView(LogoutView):
    next_page = 'homepage'

    def get(self, request, *args, **kwargs):
        messages.info(request, MSG_SUCCESS_LOGOUT)
        return super().get(request, *args, **kwargs)
