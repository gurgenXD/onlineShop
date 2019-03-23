from django.contrib import admin
from articles.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'created_date']
    list_filter = ['title', 'published', 'created_date']
    list_editable = ['created_date', 'published']


admin.site.register(Article, ArticleAdmin)