from django.db import models


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
