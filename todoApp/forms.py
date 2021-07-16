from django import forms

class MyForm(forms.Form):
    Name = forms.CharField(max_length=12)
    Email = forms.CharField(widget=forms.EmailInput)
    Password = forms.CharField(widget=forms.PasswordInput)

class SignIn(forms.Form):
    Email = forms.CharField(widget=forms.EmailInput)
    Password = forms.CharField(widget=forms.PasswordInput)