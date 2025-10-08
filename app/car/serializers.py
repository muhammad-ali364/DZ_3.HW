from rest_framework import serializers
from app.car.models import Car

class CarSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)  # генерируется автоматически
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # присваивается автоматически

    class Meta:
        model = Car
        fields = '__all__'

    def create(self, validated_data):
        """
        Присваиваем текущего пользователя только если он аутентифицирован.
        Для анонимного пользователя поле user остается пустым (null).
        """
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            validated_data['user'] = user
        return super().create(validated_data)
