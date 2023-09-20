from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        blank=False,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=False,
        validators=(
            RegexValidator(r'^[-a-zA-Z0-9_]+$', message='Неверный slug!'),
        ),
        verbose_name='Уникальный slug'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}: {self.color}'
