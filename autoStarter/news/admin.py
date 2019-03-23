from django.contrib import admin
from news.models import News

from django.urls import reverse
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'created_date']
    list_filter = ['title', 'published', 'created_date']
    list_editable = ['created_date', 'published']


admin.site.register(News, NewsAdmin)


class TinyMCEFlatPageAdmin(FlatPageAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE())
        return super(TinyMCEFlatPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)