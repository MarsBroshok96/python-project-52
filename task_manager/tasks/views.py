from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .models import Task
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from .filter import TaskFilter


MSG_NO_PERMISSION = _('You are not authorized! Please sign in')
MSG_TASK_DELETED = _('Task was deleted successfully')
MSG_NO_PERMISSION_TO_DELETE = _('You have no permission to delete this task')
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


class CustomLoginRequiredMixin(LoginRequiredMixin):

    no_permission_message = MSG_NO_PERMISSION
    login_url = 'login'
    redirect_field_name = ''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.no_permission_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class TaskListView(CustomLoginRequiredMixin, FilterView):
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = Task
    fields = ['name', 'description', 'status', 'assigned_to', 'labels']
    success_url = reverse_lazy('task_list')
    success_message = _('Task was created successfully')
    extra_context = CONTEXT_CREATE
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Task
    fields = ['name', 'description', 'status', 'assigned_to', 'labels']
    success_url = reverse_lazy('task_list')
    success_message = _('Task was updated successfully')
    extra_context = CONTEXT_UPDATE
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):

    model = Task
    success_url = reverse_lazy('task_list')
    template_name = 'tasks/task_confirm_delete.html'
    success_message = MSG_TASK_DELETED

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        if task.created_by != request.user:
            messages.error(self.request, MSG_NO_PERMISSION_TO_DELETE)
            return redirect('task_list')
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, _('Task is protected'))
            return redirect('task_list')


class TaskDetailView(CustomLoginRequiredMixin, DetailView):

    model = Task
    template_name = 'tasks/task_detail.html'
    extra_context = CONTEXT_DETAIL
