from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Category, Product, Review, Sale
from .serializers import (
    CategorySerializer, ProductSerializer, ProductFullSerializer,
    ReviewSerializer, SaleSerializer
)


@api_view(['GET'])
@csrf_exempt
def categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def catalog(request):
    try:
        current_page = int(request.GET.get('currentPage', 1))
        category_id = request.GET.get('category')
        sort = request.GET.get('sort', 'date')
        sort_type = request.GET.get('sortType', 'dec')
        limit = int(request.GET.get('limit', 20))

        name_filter = request.GET.get('name')
        min_price = request.GET.get('minPrice')
        max_price = request.GET.get('maxPrice')
        free_delivery = request.GET.get('freeDelivery')
        available = request.GET.get('available', 'true')

        products = Product.objects.filter(available=True)

        if name_filter:
            products = products.filter(title__icontains=name_filter)
        if min_price:
            products = products.filter(price__gte=float(min_price))
        if max_price:
            products = products.filter(price__lte=float(max_price))
        if free_delivery and free_delivery.lower() == 'true':
            products = products.filter(free_delivery=True)
        if category_id:
            products = products.filter(category_id=category_id)

        if sort == 'rating':
            order_field = 'rating'
        elif sort == 'price':
            order_field = 'price'
        elif sort == 'reviews':
            products = products.annotate(reviews_count=Count('reviews'))
            order_field = 'reviews_count'
        else:
            order_field = 'date'

        if sort_type == 'inc':
            order_field = order_field
        else:
            order_field = f'-{order_field}'

        products = products.order_by(order_field)

        tags = request.GET.getlist('tags')
        if tags:
            products = products.filter(tags__id__in=tags).distinct()

        paginator = Paginator(products, limit)
        try:
            page_obj = paginator.page(current_page)
        except:
            page_obj = paginator.page(1)
            current_page = 1

        serializer = ProductSerializer(page_obj.object_list, many=True)
        return Response({
            'items': serializer.data,
            'currentPage': current_page,
            'lastPage': paginator.num_pages
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'status': 'error', 'message': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@csrf_exempt
def popular_products(request):
    products = Product.objects.filter(available=True, rating__gte=4.0).order_by('-rating')[:8]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def limited_products(request):
    products = Product.objects.filter(available=True, limited_edition=True)[:16]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def sales(request):
    current_page = int(request.GET.get('currentPage', 1))
    sales = Sale.objects.select_related('product').filter(product__available=True)
    paginator = Paginator(sales, 10)
    try:
        page_obj = paginator.page(current_page)
    except:
        page_obj = paginator.page(1)
        current_page = 1
    serializer = SaleSerializer(page_obj.object_list, many=True)
    return Response({
        'items': serializer.data,
        'currentPage': current_page,
        'lastPage': paginator.num_pages
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def banners(request):
    products = Product.objects.filter(available=True).order_by('-date')[:5]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id, available=True)
        serializer = ProductFullSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@csrf_exempt
def product_review(request, id):
    try:
        product = Product.objects.get(id=id, available=True)
        data = json.loads(request.body)
        data['product'] = product.id

        if request.user.is_authenticated:
            data['user'] = request.user.id
        else:
            return Response(
                {'status': 'error', 'message': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            reviews = Review.objects.filter(product=product)
            review_serializer = ReviewSerializer(reviews, many=True)
            return Response(review_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )