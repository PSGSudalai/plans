from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from apps.BASE.managers import UserManager
from apps.BASE.models import (
    BaseModel,
    MAX_CHAR_FIELD_LENGTH,
    DEFAULT_BLANK_NULLABLE_FIELD_CONFIG,
)
from apps.PLAN_ACCESS.models import Role
from apps.BASE.model_fields import AppSingleChoiceField, AppSingleFileField
from apps.PLAN_ACCESS.helpers import EDUCATION
from django.utils import timezone
from datetime import timedelta


class ProfilePic(BaseModel):
    file = AppSingleFileField(upload_to="files/profile/images/")


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255, unique=True, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    full_name = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    entity_id = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    phone_number = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    image = models.ForeignKey(
        ProfilePic, on_delete=models.SET_NULL, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    is_working_profession = models.BooleanField(default=False)
    education = AppSingleChoiceField(
        choices_config=EDUCATION, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    current_profession = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.full_name})"


class OTP(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    otp = models.CharField(max_length=6)
