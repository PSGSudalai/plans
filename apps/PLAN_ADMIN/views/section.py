from apps.BASE.views import CUDAPIViewSet, ListAPIViewSet
from apps.PLAN_ADMIN.models import Section
from apps.PLAN_ADMIN.serializer import SectionReadSerializer, SectionWriteSerializer


class SectionListAPIView(ListAPIViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionReadSerializer

class SectionCUDAPIView(CUDAPIViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionWriteSerializer
    