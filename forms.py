from django import forms
from captcha.fields import CaptchaField

class NameForm(forms.Form):
	your_name = forms.CharField(label='', required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
	subject = forms.CharField(label='', required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Тема сообщения'}))
	message = forms.CharField(label='', required=True, min_length=20, max_length=300, widget=forms.Textarea(attrs={'placeholder': 'Сообщение'}))
	sender = forms.EmailField(label='', required=True, widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
	cc_mysel = forms.BooleanField(label='', required=False, widget=forms.TextInput(attrs={'class': 'col-lg-4'}))
	captcha = CaptchaField()