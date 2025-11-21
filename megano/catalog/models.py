from django.db import models
from django.db.models import Avg
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='categories/', verbose_name='Изображение категории')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    count = models.PositiveIntegerField(default=0, verbose_name='Количество')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(blank=True, verbose_name='Полное описание')
    free_delivery = models.BooleanField(default=False, verbose_name='Бесплатная доставка')
    limited_edition = models.BooleanField(default=False, verbose_name='Лимитированная серия')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, verbose_name='Рейтинг')

    tags = models.ManyToManyField(Tag, related_name='products', blank=True, verbose_name='Теги')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-date']

    def __str__(self):
        return self.title

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews:
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            self.rating = avg_rating or 0.0
            self.save()

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    src = models.ImageField(upload_to='products/', verbose_name='Изображение')
    alt = models.CharField(max_length=255, verbose_name='Альтернативный текст')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self):
        return f"Изображение для {self.product.title}"

class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Рейтинг'
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-date']
        unique_together = ['product', 'user']

    def __str__(self):
        return f"Отзыв от {self.user} на {self.product.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

class Sale(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sales',
        verbose_name='Товар'
    )
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена со скидкой')
    dateFrom = models.DateField(verbose_name='Дата начала акции')
    dateTo = models.DateField(verbose_name='Дата окончания акции')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return f"Акция на {self.product.title}"