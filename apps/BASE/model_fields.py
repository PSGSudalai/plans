from django.db import models
from apps.BASE.helpers import get_display_name_for_slug
from apps.BASE.models import MAX_CHAR_FIELD_LENGTH
import uuid


class BaseField:
    pass


class AppSingleChoiceField(BaseField, models.CharField):
    def __init__(self, choices_config: dict, *args, **kwargs):
        self.choices_config = choices_config
        self.options = self.choices_config["options"]

        generated_choices, max_length = [], 0
        for option in self.options:
            if self.type_of_options() in ["list_of_tuples"]:
                generated_choices.append(option)
                if len(option[0]) > max_length:
                    max_length = len(option[0])

            else:
                generated_choices.append((option, self.get_display_name(option)))
                if len(option) > max_length:
                    max_length = len(option)

        kwargs.update(
            {
                "choices": generated_choices,
                "max_length": max_length,
            }
        )
        super().__init__(*args, **kwargs)

    def get_display_name(self, option):
        return (
            self.options[option]
            if self.type_of_options() in ["dict"]
            else get_display_name_for_slug(option)
        )

    def type_of_options(self):
        _type = type(self.options).__name__

        if _type == "list":
            _option_to_consider = self.options[0]
            if (
                type(_option_to_consider) not in [str]
                and type(_option_to_consider).__name__ == "tuple"
            ):
                _type = "list_of_tuples"

        return _type

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices_config"] = self.choices_config
        return name, path, args, kwargs

    def get_default_option(self) -> None | str:
        if self.type_of_options() in ["list"]:
            return self.choices_config.get("default", self.options[0])

        if self.type_of_options() in ["list_of_tuples"]:
            return self.choices_config.get("default", self.options[0][0])

        return self.choices_config.get("default", [*self.options.keys()][0])

    def is_nullable(self) -> bool:
        return None in [*self.options, self.get_default_option()]


class AppSingleFileField(BaseField, models.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("upload_to", "files/")
        kwargs.setdefault("max_length", MAX_CHAR_FIELD_LENGTH)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if model_instance.file:
            _, extension = model_instance.file.name.split(".")
            new_filename = f"{uuid.uuid4().hex}.{extension}"

            model_instance.file.name = f"{new_filename}"

        return super().pre_save(model_instance, add)
