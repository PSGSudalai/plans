from apps.BASE.serializers import ReadSerializer, WriteSerializer
from apps.PLAN_ADMIN.models import Section


class SectionReadSerializer(ReadSerializer):
    class Meta(ReadSerializer.Meta):
        model = Section
        fields = [
            "id",
            "uuid",
            "url_name",
            "url_link",
            "status"
        ]

class SectionWriteSerializer(WriteSerializer):
    class Meta(WriteSerializer.Meta):
        model = Section
        fields =[
            "url_name",
            "url_link",
            "status"
        ]