from django.contrib import admin
from albums.models import Album, ImageInAlbum


class ImageInAlbumInline(admin.TabularInline):
    model = ImageInAlbum
    extra = 0


class AlbumAdmin(admin.ModelAdmin):
    inlines = [ImageInAlbumInline]


admin.site.register(Album, AlbumAdmin)