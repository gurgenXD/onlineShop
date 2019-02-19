from django.db import models


class FeedBack(models.Model):
    phone_or_email = models.CharField(max_length=250, verbose_name='Номер телефона или E-mail')
    name = models.CharField(max_length=250, verbose_name='Имя')
    message = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return "%s" % self.phone_or_email