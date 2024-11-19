from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters

from apps.BASE.pagination import AppPagination


REQUEST_TYPE_PERMISSION_MAPPING = {
    "POST": "create",
    "PATCH": "update",
    "GET": "retrieve",
    "DELETE": "DELETE",
}


class BaseViewSet(GenericViewSet):
    pagination_class = AppPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = "__all__"
    search_fields = []
    ordering_fields = "__all__"

    lookup_field = "uuid"
    permission_name = None

    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers
        response = None

        try:
            self.initial(request, *args, **kwargs)
            if self.permission_name:
                user_role = self.request.user.role
                if user_role:
                    permission_key = REQUEST_TYPE_PERMISSION_MAPPING.get(request.method)
                    if not user_role.has_permission(
                        self.permission_name, permission_key
                    ):
                        response = Response(
                            {"detail": "Forbidden"}, status.HTTP_403_FORBIDDEN
                        )
                else:
                    response = Response(
                        {"detail": "Unauthorized"}, status.HTTP_401_UNAUTHORIZED
                    )

            if not response:
                # Get the appropriate handler method
                if request.method.lower() in self.http_method_names:
                    handler = getattr(
                        self, request.method.lower(), self.http_method_not_allowed
                    )
                else:
                    handler = self.http_method_not_allowed

                response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class BasicViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    pass
