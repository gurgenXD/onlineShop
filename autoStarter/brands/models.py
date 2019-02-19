from django.db import models

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
