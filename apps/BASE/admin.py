from django.apps import apps
from django.contrib import admin
from django.db.models import CharField, TextField


class DefaultAdmin(admin.ModelAdmin):
    search_fields = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.search_fields = [
            field.name
            for field in model._meta.fields
            if isinstance(field, (CharField, TextField))
        ]
        if not self.search_fields:
            self.search_fields = []


def register_all_models():
    models = apps.get_models()
    for model in models:
        try:
            admin.site.register(model, DefaultAdmin)
        except admin.sites.AlreadyRegistered:
            pass


register_all_models()
