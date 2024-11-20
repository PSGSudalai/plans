from apps.BASE.views import CUDAPIViewSet, ListAPIViewSet
from apps.PLAN_ADMIN.models import PlanStep
from apps.PLAN_ADMIN.serializer import PlanStepReadSerializer, PlanStepWriteSerializer


class PlanStepListAPIView(ListAPIViewSet):
    filterset_fields=["follow_up"]
    queryset = PlanStep.objects.all()
    serializer_class = PlanStepReadSerializer


class PlanStepCUDAPIView(CUDAPIViewSet):
    queryset = PlanStep.objects.all()
    serializer_class = PlanStepWriteSerializer