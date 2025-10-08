# app/car/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from app.car.models import Car
from app.car.serializers import CarSerializer
from app.filters import CarFilter
from app.pagination import CustonPagination
from bot.bot_notify import send_car_notification_sync  # синхронная обертка


class CarViewsetsAPI(ModelViewSet):
    """
    Основной ViewSet для работы с машинами пользователя.
    """
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustonPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CarFilter
    search_fields = ["brand", "model", "number"]
    ordering_fields = ["date", "brand", "probeg"]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Car.objects.none()
        user = self.request.user
        if not user.is_authenticated:
            return Car.objects.none()
        return Car.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        user = request.user
        cache_key = f"user_cars_{user.id}"
        cars = cache.get(cache_key)
        if not cars:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            cars = serializer.data
            cache.set(cache_key, cars, timeout=60 * 5)  # 5 минут
        return Response(cars)

    def retrieve(self, request, *args, **kwargs):
        car_id = kwargs.get("pk")
        cache_key = f"car_{car_id}"
        car = cache.get(cache_key)
        if not car:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            car = serializer.data
            cache.set(cache_key, car, timeout=60 * 5)
        return Response(car)


class CarNotificationViewset(ModelViewSet):
    """
    ViewSet для создания уведомлений о машинах.
    Работает для авторизованных и анонимных пользователей.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = self.perform_create(serializer)
        return Response(self.get_serializer(car).data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Если пользователь авторизован, сохраняем с user
        user = self.request.user if self.request.user.is_authenticated else None
        car = serializer.save(user=user) if user else serializer.save()

        # Подготовка данных для уведомления
        car_data = {
            "owner": getattr(car.user, "email", "Аноним"),
            "brand": car.brand,
            "model": car.model,
            "number": car.number,
            "probeg": car.probeg,
            "carabka_transfer": car.carabka_transfer,
            "type_car": car.type_car,
            "date": car.date
        }

        # Синхронная отправка уведомления через безопасный loop
        try:
            send_car_notification_sync(car_data)
        except Exception as e:
            print(f"[Ошибка уведомления]: {e}")

        return car
