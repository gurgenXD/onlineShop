from django import forms
from repairs.models import Repair


class RepairForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RepairForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control repair-name', 'placeholder': 'Как к Вам обращаться'}))
        self.fields['phone'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control phone-input repair-phone', 'placeholder': 'Телефон для связи'}))
        self.fields['repair_date'] = forms.DateField(required=True, widget=forms.TextInput(attrs={'class': 'form-control repair-repair_date', 'type': 'date'}))
        self.fields['repair_time'] = forms.TimeField(required=True, widget=forms.TextInput(attrs={'class': 'form-control repair-repair_time', 'type': 'time'}))
        self.fields['car'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control repair-car', 'placeholder': 'Марка и модель авто'}))
        self.fields['description'] = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control repair-description', 'rows': 5, 'placeholder': 'Ваши предположения касательно поломки'}))