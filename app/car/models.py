# app/car/models.py
from django.db import models
from django.utils.text import slugify
from app.users.models import User
import re

# Выбор коробки передач
CARABKA_TRANSFER = (
    ("Автомат", "Автомат"),
    ("Механика", "Механика"),
    ("Электрокар", "Электрокар"),
)

# Тип машины
TYPE_CAR = (
    ("Седан", "Седан"),
    ("Универсал", "Универсал"),
    ("Грузовой", "Грузовой"),
)

class Car(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Если пользователь удален, car останется
        related_name='cars',
        null=True,    # Разрешаем анонимного пользователя
        blank=True
    )
    brand = models.CharField(max_length=155, verbose_name='Бренд')
    model = models.CharField(max_length=155, verbose_name='Модель')
    number = models.CharField(max_length=50, verbose_name='Номер машины')
    probeg = models.CharField(max_length=155, verbose_name='Пробег')
    carabka_transfer = models.CharField(
        max_length=50,
        verbose_name='Коробка передач',
        choices=CARABKA_TRANSFER,
        default="Автомат"
    )
    type_car = models.CharField(
        max_length=50,
        verbose_name='Тип машины',
        choices=TYPE_CAR,
        default="Седан"
    )
    date = models.CharField(max_length=100, verbose_name='Год выпуска')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Slug')

    def save(self, *args, **kwargs):
        """Создаем уникальный slug автоматически"""
        if not self.slug:
            base_slug = slugify(f"{self.brand}-{self.model}", allow_unicode=True)
            base_slug = re.sub(r'[^\w-]', '_', base_slug)
            slug = base_slug
            n = 1
            while Car.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model}"

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
        ordering = ['brand', 'model']
