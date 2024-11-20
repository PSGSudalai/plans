from apps.BASE.views import CUDAPIViewSet, ListAPIViewSet
from apps.PLAN_ADMIN.models import Share
from apps.PLAN_ADMIN.serializer import ShareReadSerializer, ShareWriteSerializer


class ShareListAPIView(ListAPIViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareReadSerializer


class ShareCUDAPIView(CUDAPIViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareWriteSerializer