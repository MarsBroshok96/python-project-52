from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Label
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import CustomLoginRequiredMixin, DeleteProtectionMixin


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


class LabelListView(CustomLoginRequiredMixin, View):
    "Label list view"
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
    "Create label view"
    model = Label
    fields = ['name']
    success_url = reverse_lazy('label_list')
    success_message = _('Label was created successfully')
    template_name = 'labels/form_label.html'
    extra_context = CONTEXT_CREATE


class LabelUpdateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      UpdateView):
    "Update label view"
    model = Label
    fields = ['name']
    success_url = reverse_lazy('label_list')
    success_message = _('Label was updated successfully')
    template_name = 'labels/form_label.html'
    extra_context = CONTEXT_UPDATE


class LabelDeleteView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      DeleteProtectionMixin,
                      DeleteView):
    "Delete label view"
    model = Label
    success_url = reverse_lazy('label_list')
    template_name = 'labels/label_confirm_delete.html'
    success_message = MSG_LABEL_DELETED
    protected_data_url = reverse_lazy('label_list')
    protected_data_msg = PROTECTED_LABEL_MSG
