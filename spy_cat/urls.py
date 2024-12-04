from django.urls import path, include
from rest_framework.routers import DefaultRouter
from spy_cat.views import SpyCatViewSet, MissionViewSet

app_name = "spy_cat"

router = DefaultRouter()
router.register("cats", SpyCatViewSet, basename="spy_cat")
router.register("missions", MissionViewSet, basename="missions")

urlpatterns = [
    path("", include(router.urls)),
]
