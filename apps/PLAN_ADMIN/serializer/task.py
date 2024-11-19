from apps.BASE.serializers import ReadSerializer, WriteSerializer
from apps.PLAN_ADMIN.models import PlanTask


class PlanTaskReadSerializer(ReadSerializer):
    class Meta(ReadSerializer.Meta):
        models=PlanTask
        fields = [
            "id",
            "uuid",
            "plan",
        ]

class PlanTaskWriteSerializer(WriteSerializer):
    class Meta(WriteSerializer.Meta):
        models = PlanTask
        fields = [
            "plan"
        ]