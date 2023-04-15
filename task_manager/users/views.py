from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.db.models import ProtectedError

MSG_REGISTERED = 'User successfully registered'
MSG_UPDATED = 'User`s info successfully updated'
MSG_UPDATE_ERROR = 'You can`t edit other users'
MSG_NO_PERMISSION = 'You are not authorized! Please sign in'
MSG_DELETED = 'User successfully Deleted'
MSG_PROTECTED_USER = 'Can\'t delete user because it used'


# Create your views here.
class CustomLoginRequiredMixin(LoginRequiredMixin):

    no_permission_message = MSG_NO_PERMISSION
    login_url = 'login'
    redirect_field_name = ''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.no_permission_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UsersListView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()[:15]
        return render(request, 'users/user_list.html', context={
            'users': users,
        })


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('user_list')
    template_name = 'users/register.html'
    success_message = MSG_REGISTERED


class UserUpdateView(CustomLoginRequiredMixin, View):
    template_name = 'users/update.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, pk=user_id)
        if request.user != user:
            messages.error(request, MSG_UPDATE_ERROR)
            return redirect('user_list')

        form = SignUpForm(instance=user)
        return render(request, self.template_name, {
            'form': form,
            'user_id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, pk=user_id)
        if request.user != user:
            return redirect('login')

        form = SignUpForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, MSG_UPDATED)
            return redirect('user_list')

        return render(request, self.template_name, {
            'form': form,
            'user_id': user_id})


class UserDeleteView(CustomLoginRequiredMixin, View):
    template_name = 'users/delete.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, pk=user_id)
        if request.user != user:
            messages.error(request, MSG_UPDATE_ERROR)
            return redirect('user_list')

        return render(request, self.template_name, {'user': user})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, pk=user_id)
        if request.user != user:
            return redirect('login')
        try:
            user.delete()
            messages.success(request, MSG_DELETED)
            return redirect('user_list')
        except ProtectedError:
            messages.error(request, MSG_PROTECTED_USER)
            return redirect('user_list')
