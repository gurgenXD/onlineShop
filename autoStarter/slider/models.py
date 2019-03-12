from django.db import models


class Slide(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    text = models.TextField(verbose_name="Текст")
    button_text = models.CharField(max_length=250, verbose_name='Текст кнопки')
    button_url = models.CharField(max_length=250, verbose_name='Ссылка кнопки')

    def get_picture_url(self, filename):
        return 'images/news/%s' % filename

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    def __str__(self):
        return '%s' % self.title
