from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


from apps.PLAN_ACCESS.models import Role, Feature, Permission
from apps.PLAN_ACCESS.views.base_view_set import BaseViewSet
from apps.BASE.pagination import AppPagination
from apps.BASE.serializers import read_serializer
from apps.PLAN_ACCESS.serializers import (
    RoleListingSerializer,
    RoleSerializer,
)
from apps.BASE.views import AppAPIView


class UserPermissionAccessAPIView(APIView):
    def get(self, request):
        user = request.user
        if user:
            role = user.role
            user_data = Role.objects.get_or_none(identity=role)
            if user_data:
                role_serilaizer_data = RoleSerializer(user_data).data
                temp = {}

                for permission in role_serilaizer_data["permissions"]:
                    feature_identity = permission["feature"]["identity"]
                    temp[feature_identity] = {
                        "create": permission["create"],
                        "update": permission["update"],
                        "retrieve": permission["retrieve"],
                        "delete": permission["delete"],
                    }

                role_serilaizer_data["permissions"] = temp

                return Response(role_serilaizer_data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RoleMetaAPIView(ListAPIView, AppAPIView):
    """View for get user-role and feature meta details."""

    def get(self, request, *args, **kwargs):
        data = {
            "feature": read_serializer(Feature, meta_fields=["id", "uuid", "identity"])(
                Feature.objects.all(), many=True
            ).data,
            # "role": read_serializer(
            #     Role,
            #     meta_fields=["id", "identity", "uuid", "created_by", "created"],
            # )(Role.objects.all(), many=True).data,
        }
        return self.send_response(data=data)


class RoleViewSet(BaseViewSet, viewsets.ModelViewSet, AppAPIView):
    """View-set for role and permission management."""

    queryset = Role.objects.all()
    lookup_field = "uuid"
    pagination_class = AppPagination
    search_fields = ["identity"]

    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action."""
        if self.action == "list":
            return RoleListingSerializer
        return RoleSerializer

    def format_response(self, data, status="success", action_code="DO_NOTHING"):
        """Helper method to format the response."""
        return Response({"data": data, "status": status, "action_code": action_code})

    def list(self, request, *args, **kwargs):
        """List all roles with formatted response."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.format_response(
                self.get_paginated_response(serializer.data).data
            )

        serializer = self.get_serializer(queryset, many=True)
        return self.format_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single role with formatted response."""
        role = self.get_object()
        serializer = self.get_serializer(role)
        return self.format_response(serializer.data)

    @action(methods=["GET"], detail=True)
    def permissions(self, request, uuid=None):
        """Get current role's permissions."""
        role = self.get_object()
        permissions = role.get_all_permissions()
        return self.format_response(permissions)

    @action(methods=["POST"], detail=True)
    def update_permissions(self, request, *args, **kwargs):
        """Update current role's permissions."""
        role = self.get_object()
        data = request.data
        role.update_all_permissions(data)
        updated_permissions = role.get_all_permissions()
        return self.format_response(
            {"detail": "permissions updated.", "permissions": updated_permissions}
        )

    def create(self, request, *args, **kwargs):
        """Create a new role and permissions."""
        permissions_data = request.data.get("role_permissions")
        identity_data = request.data.get("identity")

        if not identity_data:
            return self.format_response(
                {"detail": "role identity is required."},
                status="error",
                action_code="DISPLAY_ERROR_MESSAGES",
            )

        role, created = Role.objects.get_or_create(identity=identity_data)
        for permission in permissions_data:
            feature_id = permission.pop("feature")
            permission_data = permission.pop("feature_permissions")

            feature = Feature.objects.get_or_none(id=feature_id)
            if not feature:
                return self.format_response(
                    {"detail": "Not a valid feature"},
                    status="error",
                    action_code="DISPLAY_ERROR_MESSAGES",
                )

            Permission.objects.create(feature=feature, role=role, **permission_data)

        return self.format_response(
            RoleSerializer(role).data, status="success", action_code="DO_NOTHING"
        )

    def update(self, request, *args, **kwargs):
        """Update an existing role and its permissions."""
        role = self.get_object()
        permissions_data = request.data.get("role_permissions")
        identity_data = request.data.get("identity")

        if identity_data:
            role.identity = identity_data
            role.save()

        if permissions_data:
            for permission in permissions_data:
                feature_id = permission.pop("feature")
                permission_data = permission.pop("feature_permissions")

                feature = Feature.objects.get_or_none(id=feature_id)
                if not feature:
                    return self.format_response(
                        {"detail": f"Feature with ID {feature_id} not found."},
                        status="error",
                        action_code="DISPLAY_ERROR_MESSAGES",
                    )

                permission_obj, created = Permission.objects.update_or_create(
                    feature=feature, role=role, defaults=permission_data
                )

                if not created:
                    for key, value in permission_data.items():
                        setattr(permission_obj, key, value)
                    permission_obj.save()

        return self.format_response(
            RoleSerializer(role).data, status="success", action_code="DO_NOTHING"
        )
