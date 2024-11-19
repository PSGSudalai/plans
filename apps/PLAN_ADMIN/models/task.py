from apps.BASE.model_fields import AppSingleChoiceField
from apps.BASE.models import DEFAULT_BLANK_NULLABLE_FIELD_CONFIG, MAX_CHAR_FIELD_LENGTH, BaseModel
from apps.PLAN_ADMIN.helpers import STATUS
from django.db import models


class PlanTask(BaseModel):
    plan =models.CharField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    comment =models.CharField(max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    status = AppSingleChoiceField(choices_config=STATUS, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)


