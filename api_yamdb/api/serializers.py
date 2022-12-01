from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from reviews.models import Categories, Comments, Genres, Reviews, Titles, Users


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


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        if request.method == 'POST':
            if Reviews.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Reviews
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = '__all__'
