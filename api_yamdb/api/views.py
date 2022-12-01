from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets, mixins
from rest_framework.filters import SearchFilter
from .filters import TitlesFilter
from reviews.models import Categories, Comments, Genres, Reviews, Titles, Users
from .serializers import CategoriesSerializer, GenresSerializer, TitlesSerializer, CommentSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAdminOrReadOnly, IsAdminAuthorOrReadOnly


class TitlesViewSet(viewsets.ModelViewSet):
    """
    С помощью аннотации добавляем поле рейтинга к каждому объекту модели. 
    Метод Avg (среднее арифметическое).
    """
    queryset = Titles.objects.all().annotate(
        Avg('reviews__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly, )
    serializer_class = TitlesSerializer
    filterset_class = TitlesFilter


class CategoriesViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)


class GenresViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminAuthorOrReadOnly, )

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminAuthorOrReadOnly, )

    def get_queryset(self):
        review = get_object_or_404(Reviews, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Reviews, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
