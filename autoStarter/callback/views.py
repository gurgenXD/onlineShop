from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from callback.models import CallBack
from static_strings.models import MailToString


def callback(request):
    alert_success = False
    if request.method == "POST":
        phone = request.POST.get('phone_number')
        call_time = request.POST.get('time_to_callback')

        if phone == '':
            alert_success = False
            context = {
                'alert_success': alert_success,
            }
            return JsonResponse(context)

        if call_time == '':
            call_time = datetime.now().time().strftime('%H:%M') 
        else:
            call_time = call_time[13:]

        try:
            alert_success = True
            callback = CallBack.objects.create(phone=phone, call_time=call_time)

            current_site = get_current_site(request)
            mail_subject = 'Новый звонок на сайте: ' + current_site.domain
            message = render_to_string('callback/callback_message.html', {
                'domain': current_site.domain,
                'callback': callback,
            })
            to_email = MailToString.objects.all().first().email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
        except:
            alert_success = False

    context = {
        'alert_success': alert_success,
    }
    return JsonResponse(context)
