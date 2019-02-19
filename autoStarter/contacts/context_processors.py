from contacts.models import Phone, Messenger, SocialLink


def getting_phone(request):
    phone = Phone.objects.all().first()
    messenger = Messenger.objects.all().first()
    social_links = SocialLink.objects.all()

    context = {
        'phone': phone,
        'messenger': messenger,
        'social_links': social_links,
    }

    return context