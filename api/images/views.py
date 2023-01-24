from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from pagination import LimitOffsetPaginationParamsWithoutParams

from .serializers import ImageSerializer
from .models import Image


class ImageViewSet(
    CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet
):
    serializer_class = ImageSerializer
    queryset = Image.objects.all().order_by("id")  # required for pagination
    pagination_class = LimitOffsetPaginationParamsWithoutParams
