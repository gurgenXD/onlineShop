from django import forms
from profiles.models import Profile
from orders.models import Order


class OrderForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if user.is_authenticated:
            self.fields['full_name'] = forms.CharField(required=True, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Фамиля Имя Отчество', 'value': user.profile.full_name}))
            self.fields['phone'] = forms.CharField(required=True, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Номер телефона', 'value': user.profile.phone}))
            self.fields['postcode'] = forms.CharField(required=True, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Например, 385011', 'value': user.profile.postcode}))
            self.fields['country'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Россия', 'disabled': True, 'value': user.profile.country}))
            self.fields['region'] = forms.CharField(required=True, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Например, респ. Адыгея', 'value': user.profile.region}))
            self.fields['locality'] = forms.CharField(required=True, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Например, г. Майкоп', 'value': user.profile.locality}))
            self.fields['street'] = forms.CharField(required=True, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Название улицы', 'value': user.profile.street}))
            self.fields['house_nmb'] = forms.CharField(required=True, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '', 'value': user.profile.house_nmb}))
            self.fields['apartment_nmb'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '', 'value': user.profile.apartment_nmb}))