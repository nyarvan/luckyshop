from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название')
    full_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    position = models.PositiveIntegerField(verbose_name='Номер позиции')
    image = models.ImageField(upload_to='images/category', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('position', )
        index_together = ('slug', )

    def get_absolute_url(self):
        return reverse('shop:category_products_view', kwargs={'slug_category': self.slug})

    def __str__(self):
        return f'{self.full_name}'


class Catalog(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название')
    full_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталог'
        ordering = ('name',)
        index_together = ('slug', )

    def __str__(self):
        return f'{self.full_name}'


class TypeClothes(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name='Каталог')
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название')
    full_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to='images/catalog', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Тип одежды'
        verbose_name_plural = 'Типы одежды'
        ordering = ('catalog', 'name')
        index_together = ('slug', )

    def get_absolute_url(self):
        return reverse('shop:products_type_clothes_view', kwargs={'slug_type_clothes': self.slug})

    def __str__(self):
        return f'{self.full_name}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name='Каталог')
    type = models.ForeignKey(TypeClothes, on_delete=models.CASCADE, verbose_name='Тип одежды')
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=50)
    full_name = models.CharField(max_length=150, verbose_name='Полное название')
    image = models.ImageField(upload_to='images/products', verbose_name='Фотография')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    size = models.ManyToManyField(to='Size', verbose_name='Размеры', related_name='sizes')
    color = models.ForeignKey('Color', verbose_name='Цвет', null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, verbose_name='Описание')
    detail = models.TextField(blank=True, verbose_name='Детали')
    info = models.TextField(blank=True, verbose_name='Информация')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    special = models.BooleanField(default=False, verbose_name='Скидка')
    new_in = models.BooleanField(default=True, verbose_name='Новинка')
    old_price = models.DecimalField(blank=True, max_digits=10, decimal_places=2, null=True,
                                    verbose_name='Старая цена')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name', '-created')

    def get_absolute_url(self):
        return reverse('', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.category} {self.type} {self.name}'


class Size(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name='Каталог')
    name = models.CharField(max_length=20, verbose_name='Размер')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ('catalog', 'name')

    def __str__(self):
        return f'{self.catalog} - {self.name}'


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    value = models.IntegerField()
    css_tag = models.CharField(max_length=50, default='#ffff')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ('value', )

    def __str__(self):
        return f'{self.name}'


class OtherImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    image = models.ImageField(upload_to='images/products/other', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фотография продукта'
        verbose_name_plural = 'Фотографии продуктов'

    def __str__(self):
        return f'{self.product.name} №{self.id}'
