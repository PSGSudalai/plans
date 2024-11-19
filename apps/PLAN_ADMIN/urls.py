from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.PLAN_ADMIN.views import (
    PlanTaskAPIView
)

app_name = "cms"
API_URL_PREFIX = "api/"


router = DefaultRouter()


urlpatterns = [
    path('task/',PlanTaskAPIView.as_view())
   
] + router.urls
