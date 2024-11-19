from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, parsers
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from apps.BASE.pagination import AppPagination
from apps.BASE.serializers import AppModelSerializer, simple_serialize_queryset
from apps.BASE.views.base import AppCreateAPIView, APIViewMixin


class AppGenericViewSet(GenericViewSet):
    pass


class ListAPIViewSet(
    APIViewMixin,
    ListModelMixin,
    AppGenericViewSet,
):
    pagination_class = AppPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = []
    search_fields = []
    ordering_fields = "__all__"

    all_table_columns = {}
    all_filters_name = {}

    @action(
        methods=["GET"],
        url_path="table-meta",
        detail=False,
    )
    def get_meta_for_table_handler(self, *args, **kwargs):
        return self.send_response(data=self.get_meta_for_table())

    def get_meta_for_table(self) -> dict:
        return {}

    def get_table_columns(self) -> dict:
        return self.all_table_columns

    def get_filters_name(self) -> dict:
        return self.all_filters_name

    def serialize_for_filter(self, queryset, fields=None):
        if not fields:
            fields = ["id", "identity"]
        return simple_serialize_queryset(fields=fields, queryset=queryset)

    def serialize_choices(self, choices: list):
        from apps.BASE.helpers import get_display_name_for_slug

        return [{"id": _, "identity": get_display_name_for_slug(_)} for _ in choices]


class CreateModelMixinDebug(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AbstractLookUpFieldMixin:
    lookup_url_kwarg = "uuid"
    lookup_field = "uuid"


class CUDAPIViewSet(
    AbstractLookUpFieldMixin,
    APIViewMixin,
    CreateModelMixinDebug,
    UpdateModelMixin,
    DestroyModelMixin,
    AppGenericViewSet,
):
    @action(
        methods=["GET"],
        url_path="meta",
        detail=False,
    )
    def get_meta_for_create(self, *args, **kwargs):
        return self.send_response(data=self.get_serializer().get_meta_for_create())

    @action(
        methods=["GET"],
        url_path="meta",
        detail=True,
    )
    def get_meta_for_update(self, *args, **kwargs):
        return self.send_response(
            data=self.get_serializer(instance=self.get_object()).get_meta_for_update()
        )


def get_upload_api_view(meta_model, meta_fields=None):
    if not meta_fields:
        meta_fields = ["file", "id", "uuid"]

    class _View(AppCreateAPIView):
        class _Serializer(AppModelSerializer):
            class Meta(AppModelSerializer.Meta):
                model = meta_model
                fields = meta_fields

        parser_classes = [parsers.MultiPartParser]
        serializer_class = _Serializer

        def create(self, request, *args, **kwargs):
            file_size_limit = 500 * 1024 * 1024

            if "file" not in request.data:
                return self.send_error_response(
                    data={"detail": "File not found in the request"}
                )

            uploaded_file = request.data["file"]
            if uploaded_file.size > file_size_limit:
                return self.send_error_response(
                    data={"detail": "File size exceeds the limit of 50 MB"}
                )

            return super().create(request, *args, **kwargs)

    return _View


def get_video_upload_api_view(meta_model, meta_fields=None):
    if not meta_fields:
        meta_fields = ["file", "id", "uuid"]

    class _View(AppCreateAPIView):
        class _Serializer(AppModelSerializer):
            class Meta(AppModelSerializer.Meta):
                model = meta_model
                fields = meta_fields

        parser_classes = [parsers.MultiPartParser]
        serializer_class = _Serializer

        def create(self, request, *args, **kwargs):
            file_size_limit = 100 * 1024 * 1024

            if "file" not in request.data:
                return self.send_error_response(
                    data={"detail": "File not found in the request"}
                )

            uploaded_file = request.data["file"]
            if uploaded_file.size > file_size_limit:
                return self.send_error_response(
                    data={"detail": "File size exceeds the limit of 100 MB"}
                )

            return super().create(request, *args, **kwargs)

    return _View
