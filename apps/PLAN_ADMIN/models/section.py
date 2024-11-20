from apps.BASE.model_fields import AppSingleChoiceField
from apps.BASE.models import DEFAULT_BLANK_NULLABLE_FIELD_CONFIG, MAX_CHAR_FIELD_LENGTH, BaseModel
from django.db import models

from apps.PLAN_ADMIN.helpers import GALLARY_STATUS

class Section(BaseModel):
    url_name = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    url_link = models.URLField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    status = AppSingleChoiceField(choices_config=GALLARY_STATUS,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)