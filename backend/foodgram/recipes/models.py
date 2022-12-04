from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель для пользователей."""
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
    ]
    role = models.CharField(
        choices=ROLES,
        default=USER,
        max_length=30
    )

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    class Meta:
        ordering = ['username']


class Recipe(models.Model):
    """Модель рецептов."""
    pass


class ShoppingCart(models.Model):
    """Модель списков покупок."""
    pass


class Favorite(models.Model):
    """Модель избранных рецептов пользователя."""
    pass


class Subscription(models.Model):
    """Модель для подписок на авторов."""
    pass


class Ingredient(models.Model):
    """Модель для инградиентов."""
    pass
