from django.db import models


class Repair(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    phone = models.CharField(max_length=250, verbose_name='Телефон')
    repair_date = models.DateField(verbose_name='Дата записи')
    repair_time = models.TimeField(verbose_name='Время записи')
    car = models.CharField(max_length=250, verbose_name='Автомобиль')
    description = models.TextField(verbose_name='Описание проблемы', null=True, blank=True)

    class Meta:
        verbose_name = 'Запись на ремонт'
        verbose_name_plural = 'Записи на ремонт'

    def __str__(self):
        return '%s %s' % (self.name, self.phone)
