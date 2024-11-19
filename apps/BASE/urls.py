from rest_framework.routers import SimpleRouter
from django.urls import path

app_name = "base"
API_URL_PREFIX = "api/"


router = SimpleRouter()
urlpatterns = [] + router.urls
