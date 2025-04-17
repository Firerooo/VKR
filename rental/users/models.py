from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('buyer', 'Покупатель/Арендатор'),
        ('seller', 'Продавец/Арендодатель'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer', verbose_name="Роль")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    city = models.CharField(max_length=100, verbose_name="Город")
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Номер телефона")

    REQUIRED_FIELDS = ['role', 'first_name', 'last_name', 'city', 'phone_number']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
