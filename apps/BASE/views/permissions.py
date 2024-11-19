from django.core import exceptions
from apps.BASE.helpers import is_any_or_list1_in_list2


class HasValidPermissionMixin:
    required_permission: str | list[str] = None

    def check_permissions(self, request):
        if type(self.required_permission) == str:
            self.required_permission = [self.required_permission]

        super().check_permissions(request=request)

        if (
            request.user
            and request.user.is_authenticated
            and self.required_permission
            and not is_any_or_list1_in_list2(
                list1=self.required_permission,
                list2=self.get_organisation_user().permissions,
            )
        ):
            raise exceptions.PermissionDenied()
