from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from profiles.tokens import account_activation_token
from profiles.forms import SignUpForm, SignInForm, ForgotPasswordForm, NewPasswordForm, UpdateProfileForm, ChangePasswordForm
from orders.models import Order, OrderItem


def signout(request):
    logout(request)
    return redirect('signin')


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form1 = ChangePasswordForm(user=user, data=request.POST)
        form2 = UpdateProfileForm(user, request.POST)

        if 'profile_save' in request.POST and form2.is_valid():
            user.profile.full_name = form2.cleaned_data['full_name']
            user.profile.phone = form2.cleaned_data['phone']
            user.profile.postcode = form2.cleaned_data['postcode']
            user.profile.region = form2.cleaned_data['region']
            user.profile.locality = form2.cleaned_data['locality']
            user.profile.street = form2.cleaned_data['street']
            user.profile.house_nmb = form2.cleaned_data['house_nmb']
            user.profile.apartment_nmb = form2.cleaned_data['apartment_nmb']
            user.save()
            form1 = ChangePasswordForm(request.user)
            messages.success(request, 'Данные успешно обновлены.', extra_tags='profile_save')

        if 'user_save' in request.POST and form1.is_valid():
            password = form1.cleaned_data['new_password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=user.username, password=password)
            login(request, user)
            form2 = UpdateProfileForm(request.user)
            messages.success(request, 'Смена пароля прошла успешно.', extra_tags='user_save')
    else:
        form1 = ChangePasswordForm(request.user)
        form2 = UpdateProfileForm(request.user)

    context = {
        'form1': form1,
        'form2': form2,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def orders(request):
    user = request.user
    orders = Order.objects.filter(user=user.profile)

    PRODUCT_PER_PAGE = 10
    
    paginator = Paginator(orders, PRODUCT_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page=%s' % page.previous_page_number()
    else:
        prev_url = '' 
    
    if page.has_next():
        next_url = '?page=%s' % page.next_page_number()
    else:
        next_url = '' 

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }
    return render(request, 'profiles/orders.html', context)


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            if request.recaptcha_is_valid:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
    else:
        form = SignInForm()
    
    context = {
        'form': form,
    }

    return render(request, 'profiles/signin.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.username = form.cleaned_data['email']
            user.set_password(password)
            user.is_active = False
            user.save()
            try:
                current_site = get_current_site(request)
                mail_subject = 'Подтверждение почты'
                message = render_to_string('profiles/account_activate_message.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data['email']
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return render(request, 'profiles/account_activate_done.html')
            except:
                return render(request, 'profiles/account_activate_mail_error.html')

    else:
        form = SignUpForm()

    context = {
        'form': form,
    }

    return render(request, 'profiles/signup.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64).decode())
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'profiles/account_activate_complete.html')
    else:
        return render(request, 'profiles/account_activate_error.html')


class PasswordReset(PasswordResetView):
    form_class = ForgotPasswordForm
    template_name = 'profiles/password_reset.html'

    def form_valid(self, form):
        if self.request.recaptcha_is_valid:
            form.save()
            return render(self.request, 'profiles/password_reset_done.html', self.get_context_data())
        return render(self.request, self.template_name, self.get_context_data())

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'profiles/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = NewPasswordForm
    template_name = 'profiles/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'profiles/password_reset_complete.html'