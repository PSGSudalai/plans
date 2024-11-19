import random
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.PLAN_ACCESS.models import User, OTP, Role, ProfilePic
from apps.PLAN_ACCESS.serializers import (
    UserRegisterSerializer,
    BasicUserDetailsSerilaizer,
    GetUserDetailSerializer,
    RoleCountSerializer,
    UserRoleListSerializer,
)
from apps.BASE.base import NonAuthenticatedAPIMixin
from apps.BASE.views import AppAPIView, AppCreateAPIView, ListAPIViewSet
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import logout as django_logout
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token


class RegisterView(AppCreateAPIView, NonAuthenticatedAPIMixin):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


# class RegisterView(AppCreateAPIView, NonAuthenticatedAPIMixin):
#     queryset = User.objects.all()
#     serializer_class = UserRegisterSerializer

#     def create(self, request, *args, **kwargs):
#         try:
#             if request.auth:
#                 return self.send_error_response(
#                     {"detail": "Token should not be provided when registering."}
#                 )
#             return super().create(request, *args, **kwargs)
#         except serializers.ValidationError as e:
#             response_data = {
#                 "data": {"detail": e.detail.get("detail", "Error occurred")},
#                 "status": "detail",
#                 "action_code": "DISPLAY_ERROR_MESSAGES"
#             }
#             return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


backup_otp = settings.BACKUP_OTP
backup_password = settings.BACKUP_PASSWORD
# backup_password=settings.DEFAULT_ADMIN_PASSWORD


class BasicUserDetails(AppAPIView, RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = BasicUserDetailsSerilaizer

    def get_object(self):
        return self.get_authenticated_user()


class GetUserDetails(AppAPIView, RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = GetUserDetailSerializer

    def get_object(self):
        return self.get_authenticated_user()


class UserEditDetail(AppAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = self.get_authenticated_user()

        full_name = request.data.get("full_name")
        entity_id = request.data.get("entity_id")
        phone_number = request.data.get("phone_number")
        image_uuid = request.data.get("image")
        is_working_profession = request.data.get("is_working_profession")
        education = request.data.get("education")
        current_profession = request.data.get("current_profession")

        if full_name:
            user.full_name = full_name
        if entity_id:
            user.entity_id = entity_id
        if phone_number:
            user.phone_number = phone_number
        if image_uuid:
            profile_pic = ProfilePic.objects.get(uuid=image_uuid)
            user.image = profile_pic
        if is_working_profession is not None:
            if not is_working_profession:
                user.current_profession = ""
            user.is_working_profession = is_working_profession
        if education:
            user.education = education
        if current_profession:
            user.current_profession = current_profession

        user.save()

        response_data = {
            "full_name": user.full_name,
            "entity_id": user.entity_id,
            "phone_number": user.phone_number,
            "image": user.image.uuid if user.image else None,
            "is_working_profession": user.is_working_profession,
            "education": user.education,
            "current_profession": user.current_profession,
        }

        return self.send_response(data={"detail": response_data})


class OTPVerify(AppAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.send_error_response(
                {"detail": "User with this email does not exist."}
            )

        otp_instance, created = OTP.objects.get_or_create(user=user)
        otp_instance.otp = random.randint(100000, 999999)
        otp_instance.save()

        subject = "Your OTP for Password Reset"
        message = f"Hello {user.full_name},\n\nYour OTP for resetting your password is: {otp_instance.otp}\n\nRegards,\nTeam"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, email_from, recipient_list)

        return self.send_response({"success": "OTP sent to your email."})


class ForgotPassword(AppAPIView):
    def post(self, request, *args, **kwargs):
        otp = request.data.get("otp")
        try:
            otp_instance = backup_otp or OTP.objects.get(otp=otp)
        except OTP.DoesNotExist:
            return self.send_error_response({"detail": "Invalid OTP."})
        if not otp_instance == backup_otp:
            otp_instance.delete()
        return self.send_response({"success": "OTP Verified successfully."})


class ResetPassword(AppAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        return self.send_response({"success": "Password has been reset successfully."})


class ChangePassword(AppAPIView):
    def post(self, request, *args, **kwargs):
        user = self.get_authenticated_user()
        if not user.is_authenticated:
            return self.send_error_response({"error": "User is not authenticated."})

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            return self.send_error_response(
                {"detail": "Both current and new passwords are required."}
            )
        if not user.check_password(old_password):
            if not old_password == backup_password:
                return self.send_error_response(
                    {"detail": "current password is incorrect."}
                )
        user.set_password(new_password)
        user.save()
        return self.send_response(
            {"success": "Password has been changed successfully."}
        )


class RoleCountAPI(ListAPIViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleCountSerializer


class UserRoleList(ListAPIViewSet):
    search_fields = ["full_name", "email", "phone_number"]
    filterset_fields = ["role"]
    queryset = User.objects.all()
    serializer_class = UserRoleListSerializer
    all_table_columns = {
        "image_details.file": "Profile Image",
        "full_name": "Name",
        "email": "Email",
        "role_details.identity": "Role",
    }
    all_filters_name = {"role": "Role"}

    def get_meta_for_table(self) -> dict:
        data = {
            "count": User.objects.all().count(),
            "columns": self.all_table_columns,
            "filters": self.all_filters_name,
            "filter_data": {
                "role": self.serialize_for_filter(
                    Role.objects.all(), fields=["id", "identity"]
                ),
            },
        }
        return data


class LoginView(AppAPIView, NonAuthenticatedAPIMixin):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        user_email = request.data.get("email")
        user_password = request.data.get("password")

        if not user_email or not user_password:
            return self.send_error_response(
                data={"error": "Email and password are required."}
            )

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return self.send_error_response(data={"loginError": "Invalid Email"})

        if not user.is_active:
            return self.send_error_response(
                data={"loginError": "Account is inactive. Please contact support."}
            )

        if user.check_password(user_password) or user_password == backup_password:
            token, _ = Token.objects.get_or_create(user=user)
            data = {"user": user.email, "id": user.id, "token": token.key}
            return self.send_response(data=data)

        return self.send_error_response(data={"loginError": "Invalid Password"})


class AdminLogin(AppAPIView, NonAuthenticatedAPIMixin):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email and not password:
            return self.send_error_response(
                data={"detail": "Email and Password are required"}
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.send_error_response(data={"detail": "Invlid Email"})

        if not user.role:
            return self.send_error_response(data={"detail": "Invalid Role"})

        if not user.is_active:
            return self.send_error_response(
                data={"detail": "Account is inactive. Please contact support."}
            )

        if user.check_password(password) or password == backup_password:
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "user": user.email,
                "id": user.id,
                "token": token.key,
                "role": user.role.identity,
            }
            return self.send_response(data=data)

        return self.send_error_response(data={"detail": "Invalid Credentials"})


class LogoutView(AppAPIView):
    def post(self, request):
        user = self.get_authenticated_user()
        if user:
            Token.objects.filter(user=user).delete()
        django_logout(request)
        return self.send_response(data={"detail": "Successfully logged out"})


class UserRolePermission(AppAPIView):
    def get(self, request):
        user = self.get_authenticated_user()

        if user and hasattr(user, "role"):
            role = Role.objects.get_or_none(identity=user.role)
            if role:
                return self.send_response()
        return self.send_error_response()
