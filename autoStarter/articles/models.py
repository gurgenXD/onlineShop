from django.db import models
from datetime import datetime, date
from django.urls import reverse
from tinymce import HTMLField


class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    text = HTMLField()
    published = models.BooleanField(default=True, verbose_name='Активно')
    created_date = models.DateField(default=date.today, verbose_name='Дата создания')

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (self.id, ext)
        year = datetime.now().year
        month = datetime.now().month
        return 'images/articles/%s/%s/%s' % (year, month, filename)

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.id])

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return '%s' % self.title
