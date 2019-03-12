from django.shortcuts import render
from contacts.models import Phone, Messenger, Schedule, Email, Address, SocialLink
from partners.models import Partner
from brands.models import Brand
from news.models import News
from shop.models import Category
from slider.models import Slide


def index(request):
    phones = Phone.objects.all()
    messengers = Messenger.objects.all()
    social_links = SocialLink.objects.all()
    schedule = Schedule.objects.all()
    emails = Email.objects.all()
    addresses = Address.objects.all()
    
    partners = Partner.objects.all()
    brands = Brand.objects.all()

    slides = Slide.objects.all()
    slide_first = slides.first()
    
    last_news = News.objects.filter(published=True).order_by('-pk')[:2]
    
    context = {
        'phones': phones,
        'messengers': messengers,
        'social_links': social_links,
        'schedule': schedule,
        'emails': emails,
        'addresses': addresses,
        'partners': partners,
        'brands': brands,
        'last_news': last_news,
        'slides': slides,
        'slide_first': slide_first,
    }

    return render(request, 'landing/index.html', context)
