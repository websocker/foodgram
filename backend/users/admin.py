from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    list_editable = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = '--пусто--'


@admin.register(Follow)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    list_editable = ('user', 'author',)
    empty_value_display = '--пусто--'
