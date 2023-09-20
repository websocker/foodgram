from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name
