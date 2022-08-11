from django.db import models
from shop.models import Product

class Order(models.Model):

    DELIVERY_METHOD = [
        ('Самовывоз', 'Самовывозом'),
        ('Доставка', 'Доставкой'),
        ('Новой почтой', 'Доставка Новой почтой')
    ]

    PAYMENT_METHOD = [
        ('Наличными', 'Оплата наличными'),
        ('Картой', 'Оплата картой'),
        ('Наложенный платеж', 'Наложенным платежём')
    ]

    name = models.CharField(max_length=150, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    email = models.CharField(max_length=150, db_index=True, verbose_name='Email')
    country = models.CharField(max_length=50, verbose_name='Страна')
    city = models.CharField(max_length=50, verbose_name='Город')
    address = models.CharField(max_length=150, verbose_name='Адрес')
    delivery = models.CharField(max_length=50, choices=DELIVERY_METHOD, verbose_name='Способ доставки')
    payment = models.CharField(max_length=50, choices=PAYMENT_METHOD, verbose_name='Способ оплаты')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=True, verbose_name='Заказ активен?')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ №{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products', verbose_name='Продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    size = models.CharField(max_length=15, verbose_name='Размер')
    count = models.IntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.product.name} для заказа №{self.order.id}'

    def get_cost(self):
        return self.price * self.count
