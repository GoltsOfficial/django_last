from django.db import models


class Tag(models.Model):
    """Модель для хранения тэга"""

    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    objects = models.Manager()

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для хранения категорий"""

    title = models.CharField(max_length=200, db_index=True, verbose_name="Заголовок")
    src = models.ImageField(
        upload_to="app_shop/category/category_avatar", verbose_name="Ссылка"
    )
    alt = models.CharField(max_length=128, verbose_name="Описание")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
        verbose_name="Категоря",
    )
    objects = models.Manager()

    class Meta:
        verbose_name = "Категория-субкатегория"
        verbose_name_plural = "Категории-субкатегории"

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="banners/", verbose_name="Изображение")
    link = models.CharField(max_length=200, blank=True, verbose_name="Ссылка")
    active = models.BooleanField(default=True, verbose_name="Активный")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
        ordering = ['order']