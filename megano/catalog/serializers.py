from rest_framework import serializers
from .models import Category, Product, Tag, Review, Sale, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'parent']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['src', 'alt']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    freeDelivery = serializers.BooleanField(source='free_delivery')  # ДОБАВИТЬ ЭТУ СТРОКУ

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 'count', 'date', 'title',
            'description', 'freeDelivery', 'images', 'tags',
            'reviews', 'rating'
        ]

    def get_reviews(self, obj):
        return obj.reviews.count()

class ProductFullSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 'count', 'date', 'title',
            'description', 'fullDescription', 'freeDelivery',
            'images', 'tags', 'reviews', 'specifications', 'rating'
        ]

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        return ReviewSerializer(reviews, many=True).data

    def get_specifications(self, obj):
        return []

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'author', 'text', 'rating', 'date']

class SaleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    title = serializers.CharField(source='product.title')
    images = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images']

    def get_images(self, obj):
        images = obj.product.images.all()
        return ProductImageSerializer(images, many=True).data