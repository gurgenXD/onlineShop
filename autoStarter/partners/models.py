from django.db import models


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
