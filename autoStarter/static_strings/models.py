from django.db import models
from django.conf import settings


class MailToString(models.Model):
    email = models.EmailField(max_length=250, verbose_name='E-mail')

    class Meta:
        verbose_name = 'Кому отправлять'
        verbose_name_plural = 'Кому отправлять'

    def __str__(self):
        return '%s' % self.email


class MailFromString(models.Model):
    email_use_tls = models.BooleanField(default=True, verbose_name='EMAIL_USE_TLS')
    email_port = models.PositiveIntegerField(default=587, verbose_name='EMAIL_PORT')
    email_host = models.CharField(max_length=250, verbose_name='EMAIL_HOST')
    email_host_user = models.EmailField(max_length=250, verbose_name='EMAIL_HOST_USER')
    email_host_password = models.CharField(max_length=250, verbose_name='EMAIL_HOST_PASSWORD')

    class Meta:
        verbose_name = 'Откуда отправлять'
        verbose_name_plural = 'Откуда отправлять'

    def __str__(self):
        return '%s' % self.email_host_user

    def save(self, *args, **kwargs):
        settings.EMAIL_USE_TLS = self.email_use_tls
        settings.EMAIL_PORT = self.email_port
        settings.EMAIL_HOST = self.email_host
        settings.EMAIL_HOST_USER = self.email_host_user
        settings.EMAIL_HOST_PASSWORD = self.email_host_password
        super(MailFromString, self).save(*args, **kwargs)