from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    color = models.CharField(
        null=True,
        max_length=7,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        null=True,
        max_length=200,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
