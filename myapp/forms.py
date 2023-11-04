from django import forms
from myapp.models import CallBackRequest

class CallBackForm(forms.ModelForm):
    class Meta:
        model = CallBackRequest
        fields = ['name', 'email', 'message', 'mobile_no']

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))