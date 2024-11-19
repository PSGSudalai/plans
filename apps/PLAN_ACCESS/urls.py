from django.urls import path
from apps.PLAN_ACCESS.models import ProfilePic
from apps.PLAN_ACCESS.views import (
    LoginView,
    LogoutView,
    BasicUserDetails,
    RegisterView,
    GetUserDetails,
    UserEditDetail,
    OTPVerify,
    ForgotPassword,
    ResetPassword,
    ChangePassword,
    RoleViewSet,
    RoleMetaAPIView,
    UserPermissionAccessAPIView,
    RoleCountAPI,
    UserRoleList,
    AdminLogin,
    UserRolePermission,
)
from rest_framework.routers import SimpleRouter

from apps.BASE.views.generic import get_upload_api_view


app_name = "access"
API_URL_PREFIX = "api/"


router = SimpleRouter()
router.register(r"user-role", RoleViewSet)
router.register(r"role/count", RoleCountAPI)
router.register(r"user/list", UserRoleList)


# role List and CUD
urlpatterns = [
    # User Registeration
    path("register/", RegisterView.as_view()),
    # User Login
    path("login/", LoginView.as_view()),
    # User Login
    path("logout/", LogoutView.as_view()),
    # ADmin Login
    path("admin/login/", AdminLogin.as_view()),
    # profile pic upload
    path(
        "user/profile/image/",
        get_upload_api_view(meta_model=ProfilePic).as_view(),
    ),
    # User Details
    path("basic/details/", BasicUserDetails.as_view()),
    path("user/details/", GetUserDetails.as_view()),
    # Edit User Details
    path("user/details/edit/", UserEditDetail.as_view()),
    path("otp/verify/", OTPVerify.as_view()),
    path("forgotpassword/", ForgotPassword.as_view()),
    path("resetpassword/", ResetPassword.as_view()),
    path("changepassword/", ChangePassword.as_view()),
    path("user-role/meta/", RoleMetaAPIView.as_view()),
    path("user-role/access/", UserPermissionAccessAPIView.as_view()),
    path("user-role/permission/", UserRolePermission.as_view()),
] + router.urls
