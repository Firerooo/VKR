from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.core.validators import MinValueValidator

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username}"

class AmenityCategory(models.TextChoices):
    MAIN = "main", _("Основные")
    KITCHEN = "kitchen", _("Кухня")
    BEDROOM = "bedroom", _("Спальня")
    BATHROOM = "bathroom", _("Ванная комната")
    OTHER = "other", _("Другое")

class Amenity(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название удобства")
    category = models.CharField(max_length=20, choices=AmenityCategory.choices, verbose_name="Категория")

    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"
    
class Apartment(models.Model):
    class Status(models.TextChoices):
        RENT = "RENT", _("Аренда")
        SALE = "SALE", _("Продажа")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="apartments"
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена",
        validators=[MinValueValidator(0)]
    )
    city = models.CharField(max_length=100, verbose_name="Город")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")
    rooms = models.IntegerField(
        verbose_name="Количество комнат",
        validators=[MinValueValidator(0)]
    )
    square_meters = models.FloatField(
        verbose_name="Квадратные метры",
        validators=[MinValueValidator(0)]
    )
    max_people = models.IntegerField(
        verbose_name="Максимальное количество человек",
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    amenities = models.ManyToManyField(
        "Amenity",
        blank=True,
        related_name="apartments",
        verbose_name="Удобства"
    )
    total_views = models.PositiveIntegerField(
        default=0,
        verbose_name="Общее количество просмотров"
    )

    # Новые поля
    CURRENCY_CHOICES = [
        ('RUB', 'Рубль'),
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('DAILY', 'Сутки'),
        ('MONTHLY', 'Месяц'),
    ]
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='RUB',
        verbose_name="Валюта"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        blank=True,
        null=True,
        verbose_name="Период сдачи",
        help_text="Выберите период сдачи, если объявление — аренда (сутки или месяц)"
    )

    def __str__(self):
        return f"{self.title} - {self.get_status_display()} ({self.price}$)"

    @classmethod
    def get_cities_with_listings(cls):
        return list(
            cls.objects.values_list('city', flat=True)
            .annotate(count=Count('id'))
            .filter(count__gt=0)
            .distinct()
        )
    
class Photo(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="apartment_photos/")

class ViewHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="view_history")
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="viewed_by")
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата просмотра")

    class Meta:
        unique_together = ('user', 'apartment')

    def __str__(self):
        return f"{self.user.username} посмотрел {self.apartment.title} ({self.viewed_at})"

