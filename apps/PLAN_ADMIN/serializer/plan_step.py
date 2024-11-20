from apps.BASE.serializers import ReadSerializer, WriteSerializer, read_serializer
from apps.PLAN_ADMIN.models import PlanStep,PlanDetail


class PlanStepReadSerializer(ReadSerializer):
    plan_detail = read_serializer(PlanDetail,meta_fields=["id","uuid","plan","incharge"])(source="plandetail")
    class Meta(ReadSerializer.Meta):
        model = PlanStep
        fields = [
            "id",
            "uuid",
            "plan_detail",
            "step",
            "follow_up",
            "comment",
            "created_at"
        ]

class PlanStepWriteSerializer(WriteSerializer):
    class Meta(WriteSerializer.Meta):
        model = PlanStep
        fields = [
            "plandetail",
            "step",
            "follow_up",
            "comment"
        ]