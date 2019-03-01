from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from feedback.models import FeedBack
from static_strings.models import MailToString
from feedback.forms import FeedBackForm


def feedback(request):
    alert_success = False
    if request.method == "POST":
        form = FeedBackForm(request.POST)
        if form.is_valid():
            if request.recaptcha_is_valid:
                phone_or_email = form.cleaned_data['phone_or_email']
                name = form.cleaned_data['name']
                message = form.cleaned_data['message']
                feedback = FeedBack.objects.create(phone_or_email=phone_or_email, name=name, message=message)

                try:
                    alert_success = True
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
    else:
        form = FeedBackForm()
    
    context = {
        'alert_success': alert_success,
    }

    return JsonResponse(context)
