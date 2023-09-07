from django.contrib import admin

from recipes.models import Recipe, RecipeIngredient


class IngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_count')
    list_editable = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientsInline,)
    empty_value_display = '--пусто--'

    @staticmethod
    def favorite_count(obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')
    empty_value_display = '--пусто--'
