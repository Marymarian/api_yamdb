from rest_framework import viewsets, status, permissions, filters, serializers, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Categories, Comments, Genres, Reviews, Titles, Users
from .serializers import UsersSerializer, SignUpSerializer, GetTokenSerializer, CategoriesSerializer, GenresSerializer, TitlesSerializer, CommentSerializer, ReviewSerializer
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminAuthorOrReadOnly
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import TitlesFilter


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(methods=['get', 'patch'], detail=False, url_path='me',
            permission_classes=(permissions.IsAuthenticated,))
    def user_own_account(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save(role=user.role, partial=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user, created = Users.objects.get_or_create(username=username,
                                                email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        'noreply@yamdb.com',
        [user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(Users, username=username)
    if default_token_generator. check_token(
        user, confirmation_code
    ):
        token = str(AccessToken.for_user(user))
        return Response({'token': token}, status=status.HTTP_200_OK)
    raise serializers.ValidationError('Введен неверный код')


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
