from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = {"fullName","email","phoneNumber","adress"}
        widgets = {'fullName': forms.TextInput(attrs={'class': 'form-control'}),'email':forms.EmailInput(attrs={'class': 'form-control'}),'phoneNumber':forms.TextInput(attrs={'class': 'form-control'})}
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = {"fullName","email","phoneNumber","adress"}

class Login(forms.Form):
    email = forms.EmailField(label="E-Mail", widget=forms.EmailInput(attrs={'class': 'form-control rounded-3 my-2 '}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control mt-2 mb-4'}))

