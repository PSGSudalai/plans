from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.PLAN_ADMIN.views import (
    PlanTaskAPIView,
    PlanTaskListAPIView,
    PlanTaskCUDAPIView,
    CommentListAPIView,
    CommentCUDAPIView,
)

app_name = "cms"
API_URL_PREFIX = "api/"


router = DefaultRouter()

router.register('task/list',PlanTaskListAPIView,basename="task-list")
router.register('task/cud',PlanTaskCUDAPIView,basename="task-cud")


router.register('comment/list',CommentListAPIView,basename="comment-list")
router.register('comment/cud',CommentCUDAPIView,basename="comment-cud")


urlpatterns = [
    path('task/',PlanTaskAPIView.as_view())
   
] + router.urls
