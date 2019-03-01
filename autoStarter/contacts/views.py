from django.shortcuts import render
from contacts.models import Phone, Messenger, Schedule, Email, Address, SocialLink
from feedback.forms import FeedBackForm


def contacts(request):
    phones = Phone.objects.all()
    messengers = Messenger.objects.all()
    social_links = SocialLink.objects.all()
    schedule = Schedule.objects.all()
    emails = Email.objects.all()
    addresses = Address.objects.all()

    form = FeedBackForm()

    context = {
        'phones': phones,
        'messengers': messengers,
        'social_links': social_links,
        'schedule': schedule,
        'emails': emails,
        'addresses': addresses,
        'form': form,
    }

    return render(request, 'contacts/contacts.html', context)