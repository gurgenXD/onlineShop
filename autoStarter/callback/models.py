from django.db import models


class CallBack(models.Model):
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    call_time = models.CharField(max_length=250, verbose_name='Время звонка')

    class Meta:
        verbose_name = 'Звонок'
        verbose_name_plural = 'Звонки'

    def __str__(self):
        return '%s' % self.phone
