from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class GroceryList(models.Model):
    user = models.ForeignKey(User,
                             ...)
    recipe = models.ForeignKey(Recipe,
                               ...)

    class Meta:
        ...

    def __str__(self):
        ...


class Favorite(models.Model):
    ...


class Subscription(models.Model):
    ...
