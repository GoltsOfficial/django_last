# product/urls.py - УБЕДИТЕСЬ ЧТО ТАК
from django.urls import path, re_path
from django.views.generic import RedirectView

from .views import ProductsDetailView, ReviewProductView

urlpatterns = [
    path("product/<int:id>/", ProductsDetailView.as_view(), name="product-detail"),
    path("product/<int:id>/reviews/", ReviewProductView.as_view(), name="product-reviews"),
    re_path(r'^catalog/(?P<id>\d+)/$', RedirectView.as_view(pattern_name='product-detail', permanent=False)),
]