from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include


from images.urls import router as image_router

urlpatterns = [
    path("api/images/", include(image_router.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
