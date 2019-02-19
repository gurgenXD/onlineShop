from django.db import models
from shop.models import Product
from profiles.models import Profile


class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    full_name = models.CharField(max_length=250, verbose_name='ФИО', blank=True, null=True, default='')
    email = models.EmailField(verbose_name='E-mail', blank=True, null=True, default='')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True, null=True, default='')
    postcode = models.CharField(max_length=20, verbose_name='Индекс', blank=True, null=True, default='')
    country = models.CharField(max_length=250, default='Россия', verbose_name='Страна', blank=True, null=True)
    region = models.CharField(max_length=250, verbose_name='Регион', blank=True, null=True, default='')
    locality = models.CharField(max_length=250, verbose_name='Населенный пункт', blank=True, null=True, default='')
    street = models.CharField(max_length=250, verbose_name='Улица', blank=True, null=True, default='')
    house_nmb = models.CharField(max_length=250, verbose_name='Номер дома', blank=True, null=True, default='')
    apartment_nmb = models.CharField(max_length=250, default='', verbose_name='Номер квартиры', blank=True, null=True)
    total_price = models.PositiveIntegerField(default=0, verbose_name='Итоговая стоимость', blank=True, null=True)
    delivery = models.ForeignKey('Delivery', on_delete=models.CASCADE, verbose_name='Способ доставки', null=True, blank=True)
    status_delivery = models.ForeignKey('StatusDelivery', on_delete=models.CASCADE, verbose_name='Статус доставки')
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, verbose_name='Способ оплаты', null=True, blank=True)
    status_payment = models.ForeignKey('StatusPayment', on_delete=models.CASCADE, verbose_name='Статус оплаты')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий', default='')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    saved = models.BooleanField(default=False, verbose_name='Был сохранен')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ №%s' % self.id

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def save(self, *args, **kwargs):
        if self.status_payment.id != 1 and not self.saved:
            for item in self.items.all():
                if item.product.stock < item.quantity:
                    item.product.stock = 0
                else:
                    item.product.stock -= item.quantity
                item.product.save()
                self.saved = True
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена', blank=True, null=True)
    total_price = models.PositiveIntegerField(default=0, verbose_name='Стоимость', blank=True, null=True, help_text='Посчитается при сохранении.')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return "%s" % self.id

    def get_cost(self):
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        if self.order.status_payment != 1:   
            self.product.stock -= self.quantity
            self.product.save()
        super(OrderItem, self).save(*args, **kwargs)


class Delivery(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    address = models.CharField(max_length=250, verbose_name='Адресс', default='', null=True, blank=True)

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'

    def __str__(self):
        return "%s" % self.name


class Payment(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')

    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'

    def __str__(self):
        return "%s" % self.name
    

class StatusPayment(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')

    class Meta:
        verbose_name = 'Статус оплаты'
        verbose_name_plural = 'Статусы оплаты'

    def __str__(self):
        return "%s" % self.name


class StatusDelivery(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')

    class Meta:
        verbose_name = 'Статус доставки'
        verbose_name_plural = 'Статусы доставки'

    def __str__(self):
        return "%s" % self.name