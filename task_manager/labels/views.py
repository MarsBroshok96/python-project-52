from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Label
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


MSG_NO_PERMISSION = _('You are not authorized! Please sign in')
MSG_LABEL_DELETED = _('Label was deleted successfully')
PROTECTED_LABEL_MSG = _('Can\'t delete label because it used')
CONTEXT_CREATE = {'page_description': _('label creating page'),
                  'page_title': _('Create label'),
                  'page_h1': _('Create label'),
                  'page_btn_name': _('Create')
                  }
CONTEXT_UPDATE = {'page_description': _('label updating page'),
                  'page_title': _('Update label'),
                  'page_h1': _('Update label'),
                  'page_btn_name': _('Update')
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


class LabelListView(CustomLoginRequiredMixin, View):
    template_name = 'labels/label_list.html'

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()[:15]
        return render(request,
                      self.template_name,
                      context={'labels': labels}
                      )


class LabelCreateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      CreateView):

    model = Label
    fields = ['name']
    success_url = reverse_lazy('label_list')
    success_message = _('Label was created successfully')
    template_name = 'labels/form_label.html'
    extra_context = CONTEXT_CREATE


class LabelUpdateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      UpdateView):

    model = Label
    fields = ['name']
    success_url = reverse_lazy('label_list')
    success_message = _('Label was updated successfully')
    template_name = 'labels/form_label.html'
    extra_context = CONTEXT_UPDATE


class LabelDeleteView(CustomLoginRequiredMixin, DeleteView):

    model = Label
    success_url = reverse_lazy('label_list')
    template_name = 'labels/label_confirm_delete.html'
    success_message = MSG_LABEL_DELETED
    protected_data_url = reverse_lazy('label_list')
    protected_data_msg = PROTECTED_LABEL_MSG

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, self.protected_data_msg)
            return redirect(self.protected_data_url)
