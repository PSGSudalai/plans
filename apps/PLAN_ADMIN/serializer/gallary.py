from apps.BASE.serializers import ReadSerializer, WriteSerializer, read_serializer
from apps.PLAN_ADMIN.models import Gallary,GallaryImage


class GallaryReadSerializer(ReadSerializer):
    image_detail = read_serializer(GallaryImage,meta_fields=["id","uuid","file"])(source="image")
    class Meta(ReadSerializer.Meta):
        model = Gallary
        fields = [
            "id",
            "uuid",
            "title",
            "image_detail",
            "description",
        ]

class GallaryWriteSerializer(WriteSerializer):
    class Meta(WriteSerializer.Meta):
        model = Gallary
        fields = [
            "title",
            "image",
            "description"
        ]
        