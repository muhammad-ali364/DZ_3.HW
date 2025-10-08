import django_filters
from app.car.models import Car

class CarFilter(django_filters.FilterSet):
    date_from = django_filters.NumberFilter(field_name="date", lookup_expr="gte")
    date_from = django_filters.NumberFilter(field_name='date', lookup_expr='lte')
    brend = django_filters.CharFilter(field_name='brend', lookup_expr='icontains')
    type_car = django_filters.CharFilter(field_name='type_car',lookup_expr='type_car')

    class Meta:
        model = Car
        fields = ["brend", "type_car","carabka_transfer"]