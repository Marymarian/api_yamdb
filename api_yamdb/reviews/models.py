from django.db import models
from .validators import validate_for_year
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

ROLE_CHOICES = (
               ('user', 'Пользователь'),
               ('moderator', 'Модератор'),
               ('admin', 'Администратор'),
)


class Users(AbstractUser):
    """Кастомная модель пользователя."""
    bio = models.TextField(blank=True, verbose_name='О себе')
    role = models.CharField(choices=ROLE_CHOICES, max_length=16,
                            default='user', verbose_name='Роль')

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == 'admin'
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ('id',)


class Categories(models.Model):
    """
    Категории произведений.Произведению может быть присвоена одна категория.
    """
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Уникальный id',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    """
    Жанры произведений.Произведению может быть присвоено несколько жанров.
    """
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Уникальный id',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения, к которым пишут отзывы."""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Жанр',
        related_name='titles',
        through='Affiliation'
    )
    year = models.PositiveIntegerField(
        verbose_name='Дата выхода',
        validators=[validate_for_year]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    rating = models.PositiveIntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Affiliation(models.Model):
    """Принадлежность произведений к жанрам."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genres,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Произведение и его жанр'
        verbose_name_plural = 'Произведения и их жанры'

    def __str__(self):
        return f'{self.title} принадлежит жанру {self.genre}'



class CommentsReview(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        Users,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )    

    class Meta:
        abstract = True
    
class Review(CommentsReview):
    """Отзывы на произведения. Отзыв привязан к определённому произведению."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            ),
        )


class Comments(CommentsReview):
    """Комментарии к отзывам. Комментарий привязан к определённому отзыву."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
