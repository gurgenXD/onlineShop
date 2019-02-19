from slugify import slugify
from django.db import models
from datetime import datetime, date
from django.urls import reverse
from tinymce import HTMLField


class News(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    text = HTMLField()
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Slug')
    published = models.BooleanField(default=True, verbose_name='Активно')
    created_date = models.DateField(default=date.today, verbose_name='Дата создания')

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (self.slug, ext)
        year = datetime.now().year
        month = datetime.now().month
        return 'images/news/%s/%s/%s' % (year, month, filename)

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.title
