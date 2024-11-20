from apps.BASE.serializers import ReadSerializer, WriteSerializer, read_serializer
from apps.PLAN_ADMIN.models import PlanDetail,PlanTask


class PlanDetailReadSerializer(ReadSerializer):
    plan_detail = read_serializer(meta_model=PlanTask,meta_fields=["id","uuid","plan","status"])(source="plan")
    class Meta(ReadSerializer.Meta):
        model = PlanDetail
        fields = [
            "id",
            "uuid",
            "plan_detail",
            "incharge",
            "objective",
            "description"
        ]

class PlanDetailWriteSerializer(WriteSerializer):
    class Meta(WriteSerializer.Meta):
        model = PlanDetail
        fields = [
            "plan",
            "incharge",
            "objective",
            "description"
        ]