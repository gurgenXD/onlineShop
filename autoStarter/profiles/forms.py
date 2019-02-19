from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from profiles.models import Profile


class SignInForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш e-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'customCheck1'}))

    error_messages = {
        'invalid_login': "Пожалуйста, введите правильные e-mail и пароль. Оба поля могут быть чувствительны к регистру."
    }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш e-mail'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'}))
    password2 = forms.CharField(label='Подтвердить пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой пользователь уже существует')

        return email


class ForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш e-mail'}))


class NewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш новый пароль'}))
    new_password2 = forms.CharField(label='Подтвердить пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите новый пароль'}))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Текущий пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Текущий пароль'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(label='Подтвердить пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите новый пароль'}))


class UpdateProfileForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        if user.is_authenticated:
            self.fields['full_name'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Фамиля Имя Отчество', 'value': user.profile.full_name}))
            self.fields['phone'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Номер телефона', 'value': user.profile.phone}))
            self.fields['postcode'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Например, 385011', 'value': user.profile.postcode}))
            self.fields['country'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Россия', 'disabled': True, 'value': user.profile.country}))
            self.fields['region'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Например, респ. Адыгея', 'value': user.profile.region}))
            self.fields['locality'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Например, г. Майкоп', 'value': user.profile.locality}))
            self.fields['street'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Название улицы', 'value': user.profile.street}))
            self.fields['house_nmb'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '', 'value': user.profile.house_nmb}))
            self.fields['apartment_nmb'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '', 'value': user.profile.apartment_nmb}))