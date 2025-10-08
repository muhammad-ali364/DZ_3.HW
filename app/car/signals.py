from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from app.car.models import Car

@receiver([post_save, post_delete], sender=Car)
def clear_car_cache(sender, instance, **kwargs):
    """
    Очищаем кеш пользователя и конкретной машины после добавления или удаления.
    """
    # Если есть пользователь — очищаем его кеш
    if instance.user:
        cache.delete(f"user_cars_{instance.user.id}")

    # Очищаем кеш конкретной машины
    cache.delete(f"car_{instance.id}")
