from django.contrib.auth.models import AbstractUser
from django.db import models

USERNAME_LENGTH: int = 150
FIRST_NAME_LENGTH: int = 150
LAST_NAME_LENGTH: int = 150
EMAIL_LENGTH: int = 254
PASSWORD_LENGTH: int = 254


class User(AbstractUser):
    username = models.CharField(
        max_length=USERNAME_LENGTH,
        unique=True,
    )
    first_name = models.CharField(
        max_length=FIRST_NAME_LENGTH,
        blank=False,
    )
    last_name = models.CharField(
        max_length=LAST_NAME_LENGTH,
        blank=False,
    )
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        blank=False,
        unique=True,)
    password = models.CharField(
        max_length=PASSWORD_LENGTH,
        blank=False,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='self_subscriptions_not_allowed'
            ),
        )

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
