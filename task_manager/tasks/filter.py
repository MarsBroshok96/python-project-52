"""Filters for task list view."""

from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, BooleanFilter, ChoiceFilter
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskFilter(FilterSet):
    """Define filters for tasks list."""
    class Meta:
        model = Task
        fields = ['status', 'assigned_to']

    labels_query = Label.objects.values_list('id', 'name')
    labels = ChoiceFilter(label=_('Labels'),
                          choices=labels_query)
    self_tasks = BooleanFilter(label=_('Current user`s tasks'),
                               widget=forms.CheckboxInput,
                               method='get_self_tasks')

    def get_self_tasks(self, queryset, name, value):
        """Return tasks assigned to current user."""
        if value:
            return queryset.filter(assigned_to=self.request.user)
        return queryset
