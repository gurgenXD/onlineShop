from django.shortcuts import render
from albums.models import Album


def gallery(request):
    albums = Album.objects.all()

    context = {
        'albums': albums,
    }

    return render(request, 'albums/gallery.html', context)


def album_detail(request, album_id):
    album = Album.objects.get(id=int(album_id))

    context = {
        'album': album,
    }

    return render(request, 'albums/album.html', context)