import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=50)
    last_name = forms.CharField(label="Фамилия", max_length=50)
    middle_name = forms.CharField(label="Отчество (опционально)", max_length=50, required=False)
    city = forms.CharField(label="Город проживания", max_length=100)
    email = forms.EmailField(label="Адрес электронной почты")
    phone_number = forms.CharField(label="Номер телефона", max_length=15)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Выберите роль")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'middle_name', 'city', 'phone_number', 'role', 'password1', 'password2']
        widgets = {            
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+71234567890'
            }),}
        
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        if not phone:
            raise forms.ValidationError("Номер телефона обязателен.")
        
        pattern = r'^\+?[0-9]{10,15}$'
        if not re.match(pattern, phone):
            raise forms.ValidationError("Введите корректный номер телефона (10–15 цифр, можно с + в начале).")
        return phone
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'role', 'city']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+71234567890'
            }),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        if not phone:
            raise forms.ValidationError("Номер телефона обязателен.")

        pattern = r'^\+?[0-9]{10,15}$'
        if not re.match(pattern, phone):
            raise forms.ValidationError("Введите корректный номер телефона (10–15 цифр, можно с + в начале).")
        return phone