from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .models import Task
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from .filter import TaskFilter
from task_manager.mixins import CustomLoginRequiredMixin, DeleteProtectionMixin


MSG_TASK_DELETED = _('Task was deleted successfully')
MSG_NO_PERMISSION_TO_DELETE = _('You have no permission to delete this task')
MSG_TASK_PROTECTED = _('Can\'t delete task because it used')
CONTEXT_CREATE = {'page_description': _('task creating page'),
                  'page_title': _('Create task'),
                  'page_h1': _('Create task'),
                  'page_btn_name': _('Create')
                  }
CONTEXT_UPDATE = {'page_description': _('task updating page'),
                  'page_title': _('Update task'),
                  'page_h1': _('Update task'),
                  'page_btn_name': _('Update')
                  }
CONTEXT_DETAIL = {'page_description': _('task detail page'),
                  'page_title': _('Detail task'),
                  'page_h1': _('Task view')
                  }


class TaskListView(CustomLoginRequiredMixin, FilterView):
    "Task list view"
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    "Create task view"
    model = Task
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('task_list')
    success_message = _('Task was created successfully')
    extra_context = CONTEXT_CREATE
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    "Update task view"
    model = Task
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('task_list')
    success_message = _('Task was updated successfully')
    extra_context = CONTEXT_UPDATE
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskDeleteView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     DeleteProtectionMixin,
                     DeleteView):
    "Delete task view"
    model = Task

    success_url = reverse_lazy('task_list')
    not_modify_permission_url = reverse_lazy('task_list')
    protected_data_url = reverse_lazy('task_list')
    template_name = 'tasks/task_confirm_delete.html'
    success_message = MSG_TASK_DELETED
    protected_data_msg = MSG_TASK_PROTECTED

    owner_modify_permission = True
    owner_related_field = 'created_by'
    no_modify_permission_message = MSG_NO_PERMISSION_TO_DELETE


class TaskDetailView(CustomLoginRequiredMixin, DetailView):
    "Task detail view"
    model = Task
    template_name = 'tasks/task_detail.html'
    extra_context = CONTEXT_DETAIL
