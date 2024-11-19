from apps.BASE.serializers import ReadSerializer, WriteSerializer
from apps.PLAN_ADMIN.models import PlanTask


class PlanTaskReadSerializer(ReadSerializer):
    class Meta(ReadSerializer.Meta):
        model=PlanTask
        fields = [
            "id",
            "uuid",
            "plan",
            "status",
        ]

class PlanTaskWriteSerializer(WriteSerializer):
    class Meta(WriteSerializer.Meta):
        model = PlanTask
        fields = [
            "plan",
        ]