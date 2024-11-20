from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.BASE.views import get_upload_api_view
from apps.PLAN_ADMIN.models import GallaryImage
from apps.PLAN_ADMIN.views import (
    PlanTaskAPIView,
    PlanTaskListAPIView,
    PlanTaskCUDAPIView,
    CommentListAPIView,
    CommentCUDAPIView,
    GallaryListAPIView,
    GallaryCUDAPIView,
    SectionListAPIView,
    SectionCUDAPIView,
    ShareListAPIView,
    ShareCUDAPIView,
    PlanDetailListAPIViewSet,
    PlanDetailCUDAPIViewSet,
    PlanStepListAPIView,
    PlanStepCUDAPIView,
)

app_name = "cms"
API_URL_PREFIX = "api/"


router = DefaultRouter()

router.register('task/list',PlanTaskListAPIView,basename="task-list")
router.register('task/cud',PlanTaskCUDAPIView,basename="task-cud")


router.register('comment/list',CommentListAPIView,basename="comment-list")
router.register('comment/cud',CommentCUDAPIView,basename="comment-cud")


router.register('gallary/list',GallaryListAPIView,basename="gallary-list")
router.register('gallary/cud',GallaryCUDAPIView,basename="gallary-cud")

router.register('section/list',SectionListAPIView,basename="section-list")
router.register('section/cud',SectionCUDAPIView,basename="section-cud")

router.register('share/list',ShareListAPIView,basename="share-list")
router.register('share/cud',ShareCUDAPIView,basename="share-cud")

router.register('plan/detail/list',PlanDetailListAPIViewSet,basename="plandetail-list")
router.register('plan/detail/cud',PlanDetailCUDAPIViewSet,basename="plandetail-cud")


router.register('plan/step/list',PlanStepListAPIView,basename="planstep-list")
router.register('plan/step/cud',PlanStepCUDAPIView,basename="planstep-cud")

urlpatterns = [
    path('task/',PlanTaskAPIView.as_view()),
    path(
        "gallary/image/",
        get_upload_api_view(meta_model=GallaryImage).as_view(),
    ),
   
] + router.urls
