from apps.BASE.views import ListAPIViewSet,CUDAPIViewSet
from apps.PLAN_ADMIN.models import Comment
from apps.PLAN_ADMIN.serializer import CommentReadSerializer, CommentWriteSerializer

class CommentListAPIView(ListAPIViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentReadSerializer

class CommentCUDAPIView(CUDAPIViewSet):
    queryset = Comment.objects.all()
    serializer_class =CommentWriteSerializer
