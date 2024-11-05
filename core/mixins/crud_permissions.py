from django.core.exceptions import PermissionDenied


class MixinPermissions:

    def has_permission(self, user, action):

        if user.is_superuser:
            return True

        if action in ['create', 'update', 'delete'] and not user.groups.filter(name='Supervisor').exists():
            raise PermissionDenied("You do not have permission to access this page.")

        return True
