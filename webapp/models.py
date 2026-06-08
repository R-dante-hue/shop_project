from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Стоимость')
    image_url = models.URLField(verbose_name='Изображение')
    stock = models.IntegerField(verbose_name='Остаток', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['category__title', 'title']

    def __str__(self):
        return self.title