from django.db import models


class InfoBlock(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    text = models.CharField(max_length=250, verbose_name='Текст')

    class Meta:
        verbose_name = 'Инфо блок'
        verbose_name_plural = 'Инфо блоки'

    def __str__(self):
        return '%s' % self.title
