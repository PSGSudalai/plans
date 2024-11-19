from apps.BASE.serializers import ReadSerializer, WriteSerializer, read_serializer
from apps.PLAN_ADMIN.models import Comment,PlanTask

class CommentReadSerializer(ReadSerializer):
    plan_detail = read_serializer(PlanTask,meta_fields=["id","uuid","plan","status"])(source="plan")
    class Meta(ReadSerializer.Meta):
        model = Comment
        fields = [
            "id",
            "uuid",
            "plan_detail",
            "comment",
            "created_at",

        ]

class CommentWriteSerializer(WriteSerializer):
    class Meta(WriteSerializer.Meta):
        model = Comment
        fields = [
            "plan",
            "comment",
        ]
    