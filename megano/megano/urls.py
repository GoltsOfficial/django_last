from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include

from megano import settings

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include("frontend.urls")),
]

# if settings.DEBUG:
#     urlpatterns.extend(
#         static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     )
#
#     urlpatterns.extend(
#         static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     )
#
