from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_for_year(value):
    """Дата выхода не может быть позднее текущего года."""
    if value > timezone.now().year:
        raise ValidationError(
            (f'{value} позднее текущего года!'),
            params={'value': value},
        )
