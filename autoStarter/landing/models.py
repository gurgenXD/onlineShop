from django.db import models
from tinymce import HTMLField
from django.contrib.flatpages.models import FlatPage


class AboutUs(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    text = HTMLField(verbose_name='Текст')

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'

    def get_picture_url(self, filename):
        return 'images/about_us/%s' % filename

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    def __str__(self):
        return '%s' % self.title


class Partner(models.Model):
    name = models.CharField(max_length=250, verbose_name='Партнер')
    partner_url = models.URLField(max_length=250, verbose_name='Сайт партнера', blank=True)

    def get_picture_url(self, filename):
        return 'images/partners/%s' % filename

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'

    def __str__(self):
        return '%s' % self.name


class Brand(models.Model):
    name = models.CharField(max_length=250, verbose_name='Бренд')
    brand_url = models.URLField(max_length=250, verbose_name='Сайт бренда', blank=True)

    def get_picture_url(self, filename):
        return 'images/brands/%s' % filename

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return "%s" % self.name


class Slide(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    text = models.TextField(verbose_name="Текст", null=True, blank=True)
    button_text = models.CharField(max_length=250, verbose_name='Текст кнопки', null=True, blank=True)
    button_url = models.CharField(max_length=250, verbose_name='Ссылка кнопки', null=True, blank=True)

    def get_picture_url(self, filename):
        return 'images/news/%s' % filename

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение', null=True, blank=True)

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    def __str__(self):
        return '%s' % self.title


class InfoBlock(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    text = models.CharField(max_length=250, verbose_name='Текст')

    class Meta:
        verbose_name = 'Инфо блок'
        verbose_name_plural = 'Инфо блоки'

    def __str__(self):
        return '%s' % self.title


class OurPros(models.Model):
    text = models.CharField(max_length=250, verbose_name='Текст')

    def get_picture_url(self, filename):
        return 'images/our_pros/%s' % filename

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Наш плюс'
        verbose_name_plural = 'Наши плюсы'

    def __str__(self):
        return '%s' % self.text


class TopMenuPoint(models.Model):
    point = models.ForeignKey(FlatPage, on_delete=models.CASCADE, verbose_name='Страница')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Сортировка')

    class Meta:
        verbose_name = 'Пункт верхнего меню'
        verbose_name_plural = 'Пункты верхнего меню'
        ordering = ['my_order']

    def __str__(self):
        return '%s' % self.point.title