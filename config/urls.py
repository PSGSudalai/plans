from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("common/", include("apps.BASE.urls")),
    path("access/", include("apps.PLAN_ACCESS.urls")),
    path("cms/", include("apps.PLAN_ADMIN.urls")),
]

# Static & Media Files
# ------------------------------------------------------------------------------
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
