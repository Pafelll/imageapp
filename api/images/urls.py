from django.urls import include, path
from rest_framework import routers

from images import views

router = routers.SimpleRouter()

router.register(r"", views.ImageViewSet, basename="images")

urlpatterns = [path("", include(router.urls))]
