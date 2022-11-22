from django.urls import reverse
from django.db import models


class Item(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255)
    description = models.TextField(
        verbose_name='Описание',
        max_length=500
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=8,
        decimal_places=2,
        default=0)

    price_id = models.TextField(
        max_length=200,
        unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view-item', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Список товаров'
        ordering = ['name', 'price']


class Discount(models.Model):
    discount = models.IntegerField(
        verbose_name='Скидка в процентах',
        unique=True,
        default=0)
    discount_stripe_id = models.TextField(
        max_length=200)

    def __str__(self):
        return str(self.discount)

    class Meta:
        verbose_name = 'Скидку'
        verbose_name_plural = 'Список скидок'
        ordering = ['discount']


class Order(models.Model):
    name = models.ForeignKey(
        Item,
        verbose_name='Наименование',
        on_delete=models.CASCADE)
    quantity = models.IntegerField(
        verbose_name='Количество',
        default=0)
    discount = models.ForeignKey(
        Discount,
        verbose_name='Скидка на весь заказ в процентах (применяется едиственное наибольшее значение)',
        on_delete=models.CASCADE,
        default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Товар к оплате'
        verbose_name_plural = 'Список товаров к оплате'
        ordering = ['-discount']


class Tax(models.Model):
    type_tax = models.CharField(
        verbose_name='Наименование',
        max_length=200,
        unique=True)
    tax_rate = models.IntegerField(
        verbose_name='Значение в процентах',
        default=0)
    tax_rate_id = models.TextField(
        max_length=200,
        unique=True)

    def __str__(self):
        return str(self.type_tax)

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Список налогов'
        ordering = ['tax_rate']
