from contextlib import suppress
from rest_framework import permissions, status
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import is_success
from rest_framework.views import APIView
from apps.PLAN_ACCESS.models import Role, Feature, User
from apps.PLAN_ACCESS.serializers.role import RoleSerializer
from apps.BASE.config import API_RESPONSE_ACTION_CODES
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True

        if user and hasattr(user, "role"):
            user_role = user.role
            user_role_data = Role.objects.get_or_none(identity=user_role)
            if user_role_data:
                user_role_serializer_data = RoleSerializer(user_role_data).data
                permissions = {}
                for permission in user_role_serializer_data["role_permissions"]:
                    id = permission["feature"]
                    feature = Feature.objects.get(id=id)
                    feature_identity = feature.identity
                    # print(feature_identity)
                    # if view.action == "meta" or "get_meta_for_table_handler":
                    # print(view.action)
                    # return True
                    if feature_identity == view.feature:
                        feature_permissions = permission["feature_permissions"]
                        permissions[feature_identity] = {
                            "create": feature_permissions["create"],
                            "update": feature_permissions["update"],
                            "retrieve": feature_permissions["retrieve"],
                            "delete": feature_permissions["delete"],
                        }
                        print(view.action)
                        match (view.action):
                            case "list" | "get" | "meta" | "get_meta_for_table_handler" | "get_meta_for_update" | "partial_update":
                                if permissions[feature_identity]["retrieve"]:
                                    return True
                            case "create" | "meta" | "get_meta_for_table_handler" | "get_meta_for_update" | "partial_update":
                                if permissions[feature_identity]["create"]:
                                    return True
                            case "update" | "meta" | "get_meta_for_table_handler" | "get_meta_for_update " | "partial_update":
                                if permissions[feature_identity]["update"]:
                                    return True
                            case "delete":
                                if permissions[feature_identity]["delete"]:
                                    return True
                else:
                    raise PermissionDenied("User not authorized to perform this action")
            else:
                raise PermissionDenied("User role is not authorized")

        raise PermissionDenied("User not authenticated or role not found")


class NonAuthenticatedAPIMixin:
    # this is the auth perission
    permission_classes = [permissions.AllowAny]


class APIViewMixin:
    def get_request(self):
        return self.request

    def get_user(self):
        return self.get_request().user

    def get_authenticated_user(self):
        user = self.get_user()
        return user if user and user.is_authenticated else None

    def send_error_response(self, data=None):
        return self.send_response(data=data, status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def send_response(
        data=None,
        status_code=status.HTTP_200_OK,
        action_code="DO_NOTHING",
        **other_response_data,
    ):
        return Response(
            data={
                "data": data,
                "status": "success" if is_success(status_code) else "error",
                "action_code": action_code,
                **other_response_data,
            },
            status=status_code,
        )

    def get_app_response_schema(self, response: Response, **kwargs):
        return self.send_response(
            data=response.data, status_code=response.status_code, **kwargs
        )

    def handle_exception(self, exc):
        action_code = API_RESPONSE_ACTION_CODES["display_error_1"]
        if exc and hasattr(exc, "status_code") and exc.status_code in [401]:
            action_code = "AUTH_TOKEN_NOT_PROVIDED_OR_INVALID"

        return self.get_app_response_schema(
            super().handle_exception(exc), action_code=action_code
        )

    def list(self, request, *args, **kwargs):
        with suppress(AttributeError):
            return self.get_app_response_schema(super().list(request, *args, **kwargs))

        raise MethodNotAllowed(method=self.get_request().method)

    def retrieve(self, request, *args, **kwargs):
        with suppress(AttributeError):
            return self.get_app_response_schema(
                super().retrieve(request, *args, **kwargs)
            )

        raise MethodNotAllowed(method=self.get_request().method)

    def create(self, request, *args, **kwargs):
        with suppress(AttributeError):
            return self.get_app_response_schema(
                super().create(request, *args, **kwargs)
            )

        raise MethodNotAllowed(method=self.get_request().method)

    def update(self, request, *args, **kwargs):
        with suppress(AttributeError):
            return self.get_app_response_schema(
                super().update(request, *args, **kwargs)
            )

        raise MethodNotAllowed(method=self.get_request().method)

    def destroy(self, request, *args, **kwargs):
        with suppress(AttributeError):
            return self.get_app_response_schema(
                super().destroy(request, *args, **kwargs)
            )

        raise MethodNotAllowed(method=self.get_request().method)

    def partial_update(self, request, *args, **kwargs):
        with suppress(AttributeError):
            return self.get_app_response_schema(
                super().partial_update(request, *args, **kwargs)
            )

        raise MethodNotAllowed(method=self.get_request().method)


class AppAPIView(APIViewMixin, APIView):
    sync_action_class = None
    get_object_model = None
    serializer_class = None

    def get_valid_serializer(self, instance=None):
        assert self.serializer_class

        serializer = self.serializer_class(
            data=self.request.data,
            context=self.get_serializer_context(),
            instance=instance,
        )
        serializer.is_valid(raise_exception=True)
        return serializer

    def get_serializer_context(self):
        return {"request": self.get_request()}

    def adopt_sync_action_class(self, instance):
        assert self.sync_action_class

        success, result = self.sync_action_class(
            instance=instance, request=self.get_request()
        ).execute()

        if success:
            return self.send_response(data=result)

        return self.send_error_response(data=result)

    def get_object(self, exception=NotFound, identifier="pk"):
        if self.get_object_model:
            _object = self.get_object_model.objects.get_or_none(
                **{identifier: self.kwargs[identifier]}
            )

            if not _object:
                raise exception

            return _object

        return super().get_object()

    def choices_for_meta(self, choices: list):
        from apps.BASE.helpers import get_display_name_for_slug

        return [{"id": _, "identity": get_display_name_for_slug(_)} for _ in choices]


class AppCreateAPIView(APIViewMixin, CreateAPIView):
    def perform_create(self, serializer):
        instance = serializer.save()
        self.perform_post_create(instance=instance)

    def perform_post_create(self, instance):
        pass
