from rest_framework import serializers
from reviews.models import Categories, Genres, Titles


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Titles."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Titles
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Categories."""
    lookup_field = 'slug'

    class Meta:
        model = Categories
        fields = ('name', 'slug',)


class GenresSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Genres."""
    lookup_field = 'slug'

    class Meta:
        model = Genres
        fields = ('name', 'slug',)
