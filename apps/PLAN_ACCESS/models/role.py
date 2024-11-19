from apps.BASE.models import (
    BaseIdentityModel,
    BaseModel,
    MAX_CHAR_FIELD_LENGTH,
    DEFAULT_BLANK_NULLABLE_FIELD_CONFIG,
)
from django.db import models


class Feature(BaseIdentityModel):
    identity = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH, unique=True)

    def create_default_permissions(self):
        for role in Role.objects.all():
            role.create_default_permissions(False, self)


class Role(BaseIdentityModel):
    identity = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH, unique=True)

    def update_permission(self, feature, permissions):
        Permission.objects.filter(role=self, feature=feature).delete()
        Permission(role=self, feature=feature, **permissions).save()

    def create_default_permissions(self, permission_flag=False, specific_feature=None):
        permissions = {
            "create": permission_flag,
            "update": permission_flag,
            "retrieve": permission_flag,
            "delete": permission_flag,
        }

        if specific_feature:
            Permission(role=self, feature=specific_feature, **permissions).save()
            return

        for feature in Feature.objects.all():
            try:
                Permission(role=self, feature=feature, **permissions).save()
            except Exception as error:
                pass

    def has_permission(self, feature, operation):
        permission = Permission.objects.get(role=self, feature=feature)
        return getattr(permission, operation)

    def get_all_permissions(self):
        permissions = []
        for permission in self.permissions.all():
            feature_id = permission.feature.id
            feature_permissions = {
                "create": permission.create,
                "update": permission.update,
                "retrieve": permission.retrieve,
                "delete": permission.delete,
            }

            permissions.append(
                {"feature": feature_id, "feature_permissions": feature_permissions}
            )

        return {
            "identity": self.identity,
            "role_permissions": permissions,
            "uuid": self.uuid,
        }

    def update_all_permissions(self, permissions):
        for feature, permission in permissions.items():
            feature = Feature.objects.get_or_none(identity=feature)
            if feature:
                self.update_permission(feature, permission)


class Permission(BaseModel):
    feature = models.ForeignKey(
        to=Feature, to_field="identity", on_delete=models.CASCADE, null=True
    )
    role = models.ForeignKey(to=Role, on_delete=models.SET_NULL, null=True)
    list = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    retrieve = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "feature",
            "role",
        )
