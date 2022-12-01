from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter


from .filters import TitlesFilter
from reviews.models import Categories, Genres, Titles
from .serializers import CategoriesSerializer, GenresSerializer, TitlesSerializer

from rest_framework import mixins, viewsets


class TitlesViewSet(viewsets.ModelViewSet):
    """
    С помощью аннотации добавляем поле рейтинга к каждому объекту модели. 
    Метод Avg (среднее арифметическое).
    """
    queryset = Titles.objects.all().annotate(
        Avg('reviews__score')).order_by('name')
    #permission_classes = (IsAdminOrReadOnly, )
    serializer_class = TitlesSerializer
    filterset_class = TitlesFilter



class CategoriesViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    #permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)


class GenresViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    #permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)