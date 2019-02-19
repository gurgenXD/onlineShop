from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from feedback.models import FeedBack
from static_strings.models import MailToString


def feedback(request):
    alert_success = False
    if request.method == "POST":
        phone_or_email = request.POST.get('phone_or_email')
        sub_name = request.POST.get('sub_name')
        sub_message = request.POST.get('sub_message')
        
        try:            
            alert_success = True
            feedback = FeedBack.objects.create(phone_or_email=phone_or_email, name=sub_name, message=sub_message)

            current_site = get_current_site(request)
            mail_subject = 'Новая заявка на сайте: ' + current_site.domain
            message = render_to_string('feedback/feedback_message.html', {
                'domain': current_site.domain,
                'feedback': feedback,
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
