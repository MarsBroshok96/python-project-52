from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Status
from django.db.models import ProtectedError


MSG_NO_PERMISSION = _('You are not authorized! Please sign in')
MSG_STATUS_CREATED = _('Status successfully created')
MSG_STATUS_UPDATED = _('Status successfully updated')
MSG_STATUS_DELETED = _('Status successfully deleted')
PROTECTED_STATUS_MSG = _('Can\'t delete status because it used')

CONTEXT_CREATE = {'page_description': _('Status creating page'),
                  'page_title': _('Create status'),
                  'page_h1': _('Create status'),
                  'page_btn_name': _('Create')
                  }
CONTEXT_UPDATE = {'page_description': _('Status updating page'),
                  'page_title': _('Update status'),
                  'page_h1': _('Status updating'),
                  'page_btn_name': _('Change')
                  }


class CustomLoginRequiredMixin(LoginRequiredMixin):

    no_permission_message = MSG_NO_PERMISSION
    login_url = 'login'
    redirect_field_name = ''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.no_permission_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class StatusListView(CustomLoginRequiredMixin, View):

    template_name = 'statuses/status_list.html'

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()[:15]
        return render(request,
                      self.template_name,
                      context={'statuses': statuses}
                      )


class StatusCreateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       CreateView
                       ):
    model = Status
    fields = ('name',)
    extra_context = CONTEXT_CREATE
    success_url = reverse_lazy('status_list')
    template_name = 'statuses/form_status.html'
    success_message = MSG_STATUS_CREATED


class StatusUpdateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView
                       ):
    model = Status
    fields = ('name',)
    extra_context = CONTEXT_UPDATE
    success_url = reverse_lazy('status_list')
    template_name = 'statuses/form_status.html'
    success_message = MSG_STATUS_UPDATED


class StatusDeleteView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       DeleteView
                       ):
    model = Status
    success_url = reverse_lazy('status_list')
    template_name = 'statuses/delete_status.html'
    success_message = MSG_STATUS_DELETED
    protected_data_url = reverse_lazy('status_list')
    protected_data_msg = PROTECTED_STATUS_MSG

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, self.protected_data_msg)
            return redirect(self.protected_data_url)
