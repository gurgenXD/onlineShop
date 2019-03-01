from django import forms


class FeedBackForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FeedBackForm, self).__init__(*args, **kwargs)
        self.fields['phone_or_email'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control phone_or_email', 'placeholder': 'Ваш телефон или email'}))
        self.fields['name'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control sub_name', 'placeholder': 'Ваше имя'}))
        self.fields['message'] = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control sub_message', 'rows': 5, 'placeholder': 'Текст сообщения'}))