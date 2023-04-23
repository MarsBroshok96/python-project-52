from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth import get_user_model
from .forms import SignUpForm
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import CustomLoginRequiredMixin, DeleteProtectionMixin


User = get_user_model()

MSG_REGISTERED = _('User successfully registered')
MSG_UPDATED = _('User`s info successfully updated')
MSG_EDIT_ERROR = _('You can`t edit other users')
MSG_NO_PERMISSION = _('You are not authorized! Please sign in')
MSG_DELETED = _('User successfully Deleted')
MSG_PROTECTED_USER = _('Can\'t delete user because it used')


class UsersListView(View):
    "Users list view"
    def get(self, request, *args, **kwargs):
        users = User.objects.all()[:15]
        return render(request, 'users/user_list.html', context={
            'users': users,
        })


class SignUpView(SuccessMessageMixin, CreateView):
    "User registration view"
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'
    success_message = MSG_REGISTERED


class UserUpdateView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    "User info update view"
    model = User
    form_class = SignUpForm
    success_message = MSG_UPDATED
    success_url = reverse_lazy('user_list')
    not_modify_permission_url = reverse_lazy('user_list')
    template_name = 'users/update.html'

    owner_modify_permission = True
    owner_related_field = None
    no_modify_permission_message = MSG_EDIT_ERROR


class UserDeleteView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     DeleteProtectionMixin,
                     DeleteView):
    "User delete view"
    model = User

    success_url = reverse_lazy('user_list')
    not_modify_permission_url = reverse_lazy('user_list')
    protected_data_url = reverse_lazy('user_list')
    template_name = 'users/delete.html'
    success_message = MSG_DELETED
    protected_data_msg = MSG_PROTECTED_USER

    owner_modify_permission = True
    owner_related_field = None
    no_modify_permission_message = MSG_EDIT_ERROR
