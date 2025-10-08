from rest_framework import serializers
from app.users.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# ------------------ User Serializer ------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_active"]

# ------------------ Custom Register Serializer ------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', "first_name", "last_name", "password"]
        ref_name = "CustomRegisterSerializer"  # для Swagger

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )
        user.set_password(validated_data["password"])
        user.save()

        subject = "Добро пожаловать!"
        message = (
            f"Здравствуйте {user.first_name},\n\n"
            f"Ваш аккаунт успешно зарегистрирован.\n\n"
            f"Login: {user.email}\n"
            f"Password: {validated_data['password']}\n\n"
            f"Спасибо, что зарегистрировались!"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )

        return user

# ------------------ JWT Token Serializer ------------------
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

# ------------------ Email Sending Serializer ------------------
class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    body = serializers.CharField()
    delay = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
        help_text="Отложить выполнение в секундах"
    )
