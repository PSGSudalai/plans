from rest_framework import serializers
from apps.PLAN_ACCESS.models import User, ProfilePic, Role
from apps.BASE.serializers import ReadSerializer, read_serializer
from rest_framework.authtoken.models import Token


class UserRegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "uuid",
            "email",
            "full_name",
            "role",
            "password",
            "token",
            "entity_id",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        email = validated_data.get("email")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"detail": "User with this email already exists."}
            )

        user = User(
            full_name=validated_data.get("full_name"),
            email=validated_data.get("email"),
            entity_id=validated_data.get("entity_id"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class BasicUserDetailsSerilaizer(ReadSerializer):
    image_details = read_serializer(
        meta_model=ProfilePic, meta_fields=["id", "uuid", "file"]
    )(source="image")

    class Meta(ReadSerializer.Meta):
        model = User
        fields = [
            "id",
            "uuid",
            "full_name",
            "role",
            "entity_id",
            "email",
            "image_details",
        ]


class GetUserDetailSerializer(ReadSerializer):
    image_details = read_serializer(
        meta_model=ProfilePic, meta_fields=["id", "uuid", "file"]
    )(source="image")

    class Meta(ReadSerializer.Meta):
        model = User
        fields = [
            "id",
            "uuid",
            "full_name",
            "role",
            "entity_id",
            "image_details",
            "email",
            "phone_number",
            "image",
            "is_working_profession",
            "education",
            "current_profession",
        ]


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "entity_id",
            "phone_number",
            "role",
            "image",
            "is_working_profession",
            "education",
            "current_profession",
        ]


class RoleCountSerializer(ReadSerializer):
    no_of_users = serializers.SerializerMethodField()

    class Meta(ReadSerializer.Meta):
        model = Role
        fields = ["id", "uuid", "identity", "no_of_users"]

    def get_no_of_users(self, obj):
        return User.objects.filter(role=obj).count()


class UserRoleListSerializer(ReadSerializer):
    role_details = read_serializer(Role, meta_fields=["id", "uuid", "identity"])(
        source="role"
    )
    image_details = read_serializer(ProfilePic, meta_fields=["id", "uuid", "file"])(
        source="image"
    )

    class Meta(ReadSerializer.Meta):
        model = User
        fields = [
            "uuid",
            "full_name",
            "email",
            "image_details",
            "role_details",
        ]
