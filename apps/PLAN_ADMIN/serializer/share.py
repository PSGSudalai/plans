from apps.BASE.serializers import ReadSerializer, WriteSerializer
from apps.PLAN_ADMIN.models import Share


class ShareReadSerializer(ReadSerializer):
    class Meta(ReadSerializer.Meta):
        model = Share
        fields = [
            "id",
            "uuid",
            "title",
            "mode",
            "description",
            "url",
            "username",
            "password",
            "p1_name",
            "p1_phone_number",
            "s1_name",
            "s1_phone_number",
            "t1_name",
            "t1_phone_number"
        ]

class ShareWriteSerializer(WriteSerializer):
    class Meta(WriteSerializer.Meta):
        model = Share
        fields = [
            "title",
            "mode",
            "description",
            "url",
            "username",
            "password",
            "p1_name",
            "p1_phone_number",
            "s1_name",
            "s1_phone_number",
            "t1_name",
            "t1_phone_number"
        ]