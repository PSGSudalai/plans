from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_pincode(value):
    if value > 999999 or value <= 100000:
        raise ValidationError("Pincode must have only 6 digits.")


# def validate_future_date(value):
#     if value and value < timezone.now().date():
#         raise ValidationError("Date must be in the future.")


# def validate_past_date(value):
#     if value and value > timezone.now().date():
#         raise ValidationError("Date must be in the past.")


def validate_future_today_date(value):
    if value and value <= timezone.now().date():
        raise ValidationError("Date must be in the future or today.")
