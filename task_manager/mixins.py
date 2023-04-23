from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy


MSG_NO_PERMISSION = _('You are not authorized! Please sign in')
MSG_PROTECTED = _('Can\'t delete because it used')


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Check if user is authenticated and redirect to login page if not.
    Also have flag owner_modify_permission, if True, check if user is owner
    of object and redirect to not_modify_permission_url if not.
    """
    no_permission_message = MSG_NO_PERMISSION
    no_modify_permission_message = MSG_NO_PERMISSION
    login_url = 'login'
    not_modify_permission_url = reverse_lazy('homepage')
    redirect_field_name = ''
    owner_modify_permission = False
    owner_related_field = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.no_permission_message)
            return self.handle_no_permission()
        if self.owner_modify_permission:
            if self.owner_related_field is None:
                "Case means that object is user and no extra field for owner"
                owner = self.get_object()
            else:
                "Case means that owner is object.owner_related_field"
                owner = getattr(self.get_object(), self.owner_related_field)
            if owner != request.user:
                messages.error(self.request, self.no_modify_permission_message)
                return redirect(self.not_modify_permission_url)
        return super().dispatch(request, *args, **kwargs)


class DeleteProtectionMixin:
    """
    Protect from deleting object if it used in other objects.
    If object is protected, redirect to protected_data_url and show
    protected_data_msg.
    """

    protected_data_msg = MSG_PROTECTED
    protected_data_url = reverse_lazy('homepage')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, self.protected_data_msg)
            return redirect(self.protected_data_url)
