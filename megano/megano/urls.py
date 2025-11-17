# megano/urls.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from megano import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    # API routes FIRST
    path("api/", include("accounts.urls")),
    path("api/", include("shop.urls")),
    path("api/", include("product.urls")),
    path("api/", include("cart.urls")),
    path("api/", include("order.urls")),
    path("api/", include("order.urls")),
    path('catalog/<int:id>/', RedirectView.as_view(url='/product/%(id)s/')),

    # Frontend LAST (catch-all)
    path("", include("frontend.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)