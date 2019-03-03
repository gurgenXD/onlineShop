from django.db import models
from django.urls import reverse
from slugify import slugify
import math


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, verbose_name='Подкатегория')
    name = models.CharField(max_length=250, verbose_name='Название')
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE, verbose_name='Производитель', related_name='products')
    price_without_sale = models.PositiveIntegerField(default=0, verbose_name='Цена без скидки')
    sale = models.PositiveIntegerField(default=0, verbose_name='Скидка')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена', help_text='Посчитается при сохранении')
    slug = models.SlugField(max_length=250, verbose_name='Slug', unique=True, null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    cars_list = models.TextField(verbose_name='Список автомобилей')
    cars = models.ManyToManyField('Car', verbose_name='Автомобили', blank=True, related_name='products')
    stock = models.PositiveIntegerField(default=0, verbose_name='На складе')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    purchased = models.PositiveIntegerField(default=0, verbose_name='Куплено')

    def get_main_image(self):
        return self.images.get(is_main=True)

    def get_absolute_url(self):
        return reverse('product', args=[self.category.slug, self.subcategory.slug, self.slug])

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return '%s' % (self.name)

    def save(self, *args, **kwargs):
        self.category = self.subcategory.category
        self.slug = slugify(self.subcategory.name + '-' + self.name)
        self.price = math.ceil(self.price_without_sale * (1 - self.sale/100))
        super(Product, self).save(*args, **kwargs)


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар', related_name='images')

    def get_picture_url(self, filename):
        return 'images/shop/%s/%s' % (self.product.slug, filename)

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')
    is_main = models.BooleanField(default=False, verbose_name='Главное изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return "%s" % self.id


class Feature(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return "%s" % self.name


class FeatureValue(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар', related_name='feature_values')
    feature = models.ForeignKey('Feature', on_delete=models.CASCADE, verbose_name='Характеристика', related_name='feature_values')
    value = models.CharField(max_length=250, verbose_name='Значение')

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = 'Значения характеристик'
        ordering = ['feature']

    def __str__(self):
        return "%s %s" % (self.feature.name, self.value)


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название', unique=True)
    slug = models.SlugField(max_length=250, verbose_name='Slug', unique=True, default='', help_text='Заполнится при сохранении')

    def get_absolute_url(self):
        return reverse('category', args=[self.slug])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return "%s" % self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория', related_name='subcategories')
    name = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(max_length=250, verbose_name='Slug', unique=True, default='')

    def get_absolute_url(self):
        return reverse('subcategory', args=[self.category.slug, self.slug])

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return "%s" % self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category.name + '-' + self.name)
        super(SubCategory, self).save(*args, **kwargs)


class Manufacturer(models.Model):
    name = models.CharField(max_length=250, verbose_name='Производитель товара')
    slug = models.CharField(max_length=250, verbose_name='Slug', unique=True)

    class Meta:
        verbose_name = 'Производитель товара'
        verbose_name_plural = 'Производители товаров'

    def __str__(self):
        return "%s" % self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Manufacturer, self).save(*args, **kwargs)


class Car(models.Model):
    brand = models.ForeignKey('CarBrand', on_delete=models.CASCADE, verbose_name='Марка автомобиля', related_name='cars')
    car_model = models.ForeignKey('CarModel', on_delete=models.CASCADE, verbose_name='Модель автомобиля', related_name='cars')
    release_date = models.PositiveIntegerField(verbose_name='Год выпуска')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['car_model']

    def __str__(self):
        return "%s - %s" % (self.car_model, self.release_date)


class CarBrand(models.Model):
    name = models.CharField(max_length=250, verbose_name='Марка автомобиля')

    class Meta:
        verbose_name = 'Марка автомобиля'
        verbose_name_plural = 'Марки автомобилей'

    def __str__(self):
        return "%s" % self.name


class CarModel(models.Model):
    brand = models.ForeignKey('CarBrand', on_delete=models.CASCADE, verbose_name='Марка автомобиля', related_name='cars_models')
    name = models.CharField(max_length=250, verbose_name='Модель автомобиля')


    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобиля'
        ordering = ['brand']

    def __str__(self):
        return "%s %s" %  (self.brand, self.name)