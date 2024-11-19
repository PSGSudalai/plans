from apps.BASE.views.generic import CUDAPIViewSet, ListAPIViewSet
from apps.PLAN_ADMIN.models import Gallary
from apps.PLAN_ADMIN.serializer.gallary import GallaryReadSerializer,GallaryWriteSerializer


class GallaryListAPIView(ListAPIViewSet):
    queryset = Gallary.objects.all()
    serializer_class = GallaryReadSerializer

class GallaryCUDAPIView(CUDAPIViewSet):
    queryset = Gallary.objects.all()
    serializer_class = GallaryWriteSerializer
