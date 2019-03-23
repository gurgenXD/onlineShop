from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from static_strings.models import MailToString

from contacts.models import Phone, Messenger, Schedule, Email, Address, SocialLink
from landing.models import Partner, Brand, Slide, InfoBlock, AboutUs, OurPros
from news.models import News
from shop.models import Category
from repairs.forms import RepairForm
from repairs.models import Repair
from profiles.decorators import check_recaptcha


@check_recaptcha
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

    info_blocks = InfoBlock.objects.all()

    main_info = AboutUs.objects.all().first()

    proses = OurPros.objects.all()

    last_news = News.objects.filter(published=True).order_by('-pk')[:2]
    
    alert_success2 = 1 # по умолчанию
    if request.method == "POST":
        form2 = RepairForm(request.POST)
        if form2.is_valid():
            if request.recaptcha_is_valid:
                name = form2.cleaned_data['name']
                phone = form2.cleaned_data['phone']
                repair_date = form2.cleaned_data['repair_date']
                repair_time = form2.cleaned_data['repair_time']
                car = form2.cleaned_data['car']
                description = form2.cleaned_data['description']

                repair = Repair.objects.create(
                    phone=phone,
                    name=name,
                    repair_date=repair_date,
                    repair_time=repair_time,
                    car=car,
                    description=description,
                )
                
                try:
                    current_site = get_current_site(request)
                    mail_subject = 'Новая заявка на сайте: ' + current_site.domain
                    message = render_to_string('repairs/repair_message.html', {
                        'domain': current_site.domain,
                        'repair': repair,
                    })
                    to_email = MailToString.objects.first().email
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()
                    alert_success2 = 2 # письмо не отправлено
                except:
                    alert_success2 = 3 # письмо отправлено
            else:
                alert_success2 = 0 # неправильная рекапча
    else:
        form2 = RepairForm()

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
        'info_blocks': info_blocks,
        'main_info': main_info,
        'proses': proses,
        'form2': form2,
        'alert_success2': alert_success2,
    }

    return render(request, 'landing/index.html', context)
