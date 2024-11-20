from apps.BASE.views import CUDAPIViewSet, ListAPIViewSet
from apps.PLAN_ADMIN.models import PlanDetail
from apps.PLAN_ADMIN.serializer import PlanDetailReadSerializer, PlanDetailWriteSerializer


class PlanDetailListAPIViewSet(ListAPIViewSet):
    queryset = PlanDetail.objects.all()
    serializer_class = PlanDetailReadSerializer

class PlanDetailCUDAPIViewSet(CUDAPIViewSet):
    queryset = PlanDetail.objects.all()
    serializer_class = PlanDetailWriteSerializer