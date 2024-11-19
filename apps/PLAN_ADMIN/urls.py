from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.PLAN_ADMIN.views import (
    PlanTaskAPIView,
    PlanTaskListAPIView,
    PlanTaskCUDAPIView,
)

app_name = "cms"
API_URL_PREFIX = "api/"


router = DefaultRouter()

router.register('task/list',PlanTaskListAPIView,basename="task-list")
router.register('task/cud',PlanTaskCUDAPIView,basename="task-cud")


urlpatterns = [
    path('task/',PlanTaskAPIView.as_view())
   
] + router.urls
