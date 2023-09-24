from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()
TAG_NAME_MAX_LENGTH: int = 200
TAG_SLUG_MAX_LENGTH: int = 200
TAG_COLOR_MAX_LENGTH: int = 7
INGREDIENT_NAME_MAX_LENGTH: int = 200
INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH: int = 200
RECIPE_NAME_MAX_LENGTH: int = 200
MIN_COOKING_TIME_VALUE: int = 1


class Tag(models.Model):
    name = models.CharField(
        max_length=TAG_NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=TAG_COLOR_MAX_LENGTH,
        blank=False,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        max_length=TAG_SLUG_MAX_LENGTH,
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


class Ingredient(models.Model):
    name = models.CharField(
        max_length=INGREDIENT_NAME_MAX_LENGTH,
        db_index=True,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список id тегов'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=False,
        verbose_name='Изображение',
    )
    name = models.CharField(
        max_length=RECIPE_NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                MIN_COOKING_TIME_VALUE,
                'Время приготовления не может быть меньше, чем 1 минута!'
            ),
        ),
        verbose_name='Время приготовления (в минутах)'
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
        verbose_name='Рецепты'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты'
    )
    amount = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Содержимое рецепта'
        verbose_name_plural = 'Содержимое рецептов'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            ),
        )

    def __str__(self):
        return f'{self.ingredient}: {self.amount}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        default_related_name = 'shopping_cart'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'{self.user}\'s {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        default_related_name = 'favorites'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_favorite'
            ),
        )

    def __str__(self):
        return self.recipe
