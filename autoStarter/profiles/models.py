from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    full_name = models.CharField(max_length=250, blank=True, verbose_name='ФИО')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    postcode = models.CharField(max_length=20, blank=True, verbose_name='Индекс')
    country = models.CharField(max_length=250, default='Россия', blank=True, verbose_name='Страна')
    region = models.CharField(max_length=250, blank=True, verbose_name='Регион')
    locality = models.CharField(max_length=250, blank=True, verbose_name='Населенный пункт')
    street = models.CharField(max_length=250, blank=True, verbose_name='Улица')
    house_nmb = models.CharField(max_length=250, blank=True, verbose_name='Номер дома')
    apartment_nmb = models.CharField(max_length=250, blank=True, verbose_name='Номер квартиры')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return '%s' % self.user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()