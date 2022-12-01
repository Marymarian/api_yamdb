import django_filters
from reviews.models import Titles


class TitlesFilter(django_filters.FilterSet):
    """Класс для фильтрации обьектов Titles."""
    genre = django_filters.CharFilter(field_name='genre', lookup_expr='slug')
    category = django_filters.CharFilter(field_name='category',
                                         lookup_expr='slug')
    year = django_filters.NumberFilter(field_name='year')
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    class Meta:
        model = Titles
        fields = ('genre', 'category', 'year', 'name', )