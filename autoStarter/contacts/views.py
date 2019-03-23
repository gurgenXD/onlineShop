from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from static_strings.models import MailToString

from contacts.models import Phone, Messenger, Schedule, Email, Address, SocialLink
from feedback.forms import FeedBackForm
from repairs.forms import RepairForm
from repairs.models import Repair
from profiles.decorators import check_recaptcha

@check_recaptcha
def contacts(request):
    phones = Phone.objects.all()
    messengers = Messenger.objects.all()
    social_links = SocialLink.objects.all()
    schedule = Schedule.objects.all()
    emails = Email.objects.all()
    addresses = Address.objects.all()

    alert_success = 1 # по умолчанию
    alert_success2 = 1 # по умолчанию
    if request.method == "POST":
        form = FeedBackForm(request.POST)
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
                    alert_success = 1
                except:
                    alert_success2 = 3 # письмо отправлено
                    alert_success = 1
            else:
                alert_success2 = 0 # неправильная рекапча
                alert_success = 1

        if form.is_valid():
            if request.recaptcha_is_valid:
                phone_or_email = form.cleaned_data['phone_or_email']
                name = form.cleaned_data['name']
                message = form.cleaned_data['message']
                feedback = FeedBack.objects.create(phone_or_email=phone_or_email, name=name, message=message)

                try:
                    current_site = get_current_site(request)
                    mail_subject = 'Новая заявка на сайте: ' + current_site.domain
                    message = render_to_string('feedback/feedback_message.html', {
                        'domain': current_site.domain,
                        'feedback': feedback,
                    })
                    to_email = MailToString.objects.first().email
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()
                    alert_success = 2 # письмо не отправлено
                    alert_success2 = 1
                except:
                    alert_success = 3
                    alert_success2 = 1
            else:
                alert_success = 0 # неправильная рекапча
                alert_success2 = 1
    else:
        form = FeedBackForm()
        form2 = RepairForm()

    context = {
        'phones': phones,
        'messengers': messengers,
        'social_links': social_links,
        'schedule': schedule,
        'emails': emails,
        'addresses': addresses,
        'form': form,
        'form2': form2,
        'alert_success2': alert_success2,
        'alert_success': alert_success,
    }

    return render(request, 'contacts/contacts.html', context)