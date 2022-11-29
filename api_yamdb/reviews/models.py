from django.db import models
from .validators import validate_for_year


class Categories(models.Model):
    """Категории произведений.Произведению может быть присвоена одна категория."""
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
    """Жанры произведений.Произведению может быть присвоено несколько жанров."""
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


class Titles(models.Model):
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
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=[validate_for_year]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    rating = models.IntegerField(
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
        Titles,
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