from django.db import models
from tinymce import HTMLField


class AboutUs(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    text = HTMLField(verbose_name='Текст')

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'

    def get_picture_url(self, filename):
        return 'images/news/%s' % filename

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    def __str__(self):
        return '%s' % self.title
