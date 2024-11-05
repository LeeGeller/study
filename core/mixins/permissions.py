from audioop import reverse

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class UserIsAuthorizedMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('users:login'))
        return super().dispatch(request, *args, **kwargs)


class UserIsSupervisorMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name='Supervisor').exists():
            raise PermissionDenied("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)
