from rest_framework.routers import DefaultRouter
from app.car.views import CarViewsetsAPI, CarNotificationViewset  # ✅ правильное имя

router = DefaultRouter()
router.register('car', CarViewsetsAPI, basename='car')
router.register('car-notification', CarNotificationViewset, basename='notification')

urlpatterns = router.urls  # можно сразу присвоить router.urls
