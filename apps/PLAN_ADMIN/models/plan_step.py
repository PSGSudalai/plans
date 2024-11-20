from apps.BASE.model_fields import AppSingleChoiceField
from apps.BASE.models import DEFAULT_BLANK_NULLABLE_FIELD_CONFIG, MAX_CHAR_FIELD_LENGTH, BaseModel
from django.db import models

from apps.PLAN_ADMIN.helpers import STATUS
from apps.PLAN_ADMIN.models import PlanDetail

class PlanStep(BaseModel):
    plandetail = models.ForeignKey(PlanDetail,on_delete=models.SET_NULL,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    step = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    follow_up = AppSingleChoiceField(choices_config=STATUS,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    comment = models.TextField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
