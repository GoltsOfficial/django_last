# product/views.py - ПОЛНАЯ РЕАЛИЗАЦИЯ
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, Review
from product.serializers import ProductSerializer, ReviewsSerializer


class ProductsDetailView(APIView):
    """View для детальной страницы товара"""

    def get(self, request: HttpRequest, id: int) -> Response:
        try:
            # Оптимизируем запросы с prefetch_related и select_related
            product = Product.objects.select_related(
                'category'
            ).prefetch_related(
                'images',
                'tags',
                'reviews',
                'specifications'
            ).get(pk=id, available=True)

            serializer = ProductSerializer(product)
            return Response(serializer.data)

        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReviewProductView(APIView):
    """View для отзывов товара"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request: HttpRequest, id: int) -> Response:
        """Получить отзывы товара"""
        try:
            product = Product.objects.get(pk=id, available=True)
            reviews = product.reviews.all()
            serializer = ReviewsSerializer(reviews, many=True)
            return Response(serializer.data)

        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request: HttpRequest, id: int) -> Response:
        """Добавить отзыв к товару"""
        try:
            product = Product.objects.get(pk=id, available=True)
            serializer = ReviewsSerializer(
                data=request.data,
                context={'product_id': id}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )