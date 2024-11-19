from apps.PLAN_ACCESS.models import Role, Permission, Feature, User
from apps.BASE.serializers import read_serializer
from rest_framework import serializers


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["identity", "id"]


class PermissionSerializer(serializers.ModelSerializer):
    feature_permissions = serializers.SerializerMethodField()
    feature = serializers.IntegerField(source="feature.id")

    class Meta:
        model = Permission
        fields = ["feature", "feature_permissions"]

    def get_feature_permissions(self, obj):
        return {
            "create": obj.create,
            "update": obj.update,
            "retrieve": obj.retrieve,
            "delete": obj.delete,
        }


class RoleSerializer(serializers.ModelSerializer):
    role_permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ["uuid", "identity", "role_permissions"]

    def get_role_permissions(self, obj):
        permissions = Permission.objects.filter(role=obj)
        return PermissionSerializer(permissions, many=True).data


class RoleListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            "identity",
            "uuid",
        ]
