from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect

# Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Project API",
        default_version='v1',
        description="Документация API для проекта",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# 👇 Добавляем функцию для главной страницы
def home(request):
    # Можно просто текст
    # return HttpResponse("<h1>Добро пожаловать!</h1><p>Здесь можно заказать машину.</p>")

    # 👇 Или сделать редирект прямо в Swagger или API машин:
    return redirect('/swagger/')  # можно заменить на /api/v1/car/

urlpatterns = [
    # Главная страница
    path('', home, name='home'),

    # Django admin
    path('admin/', admin.site.urls),

    # API приложения
    path("api/v1/users/", include("app.users.urls")),
    path("api/v1/car/", include("app.car.urls")),

    # Аутентификация
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("auth/github/", include("allauth.socialaccount.urls")),
    path("auth/google/", include("allauth.socialaccount.urls")),
    path("accounts/", include("allauth.urls")),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Статика и медиа
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
