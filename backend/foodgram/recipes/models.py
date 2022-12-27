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

    is_subscribed = models.BooleanField(default=False)

    class Meta:
        ordering = ['username']


class Ingredient(models.Model):
    """Модель для инградиентов."""
    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(max_length=30)


class Tag(models.Model):
    """Модель для тегов."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=10)


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        related_name='author',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        'Рецепт',
        max_length=200,
        help_text='Введите название рецепта'
    )
    image = models.TextField(
        verbose_name='Изображение блюда',
        help_text='Картинка, закодированная в Base64'
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
        help_text='Заполните текстовое описание'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в мин.',
        help_text='Заполните время приготовления'
    )


class RecipeIngredients(models.Model):
    """Модель связи рецепта с инградиентами."""
    recipe = models.ForeignKey(
        Recipe,
        null=True,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        null=True,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField()


class ShoppingCart(models.Model):
    """Модель списков покупок."""
    user = models.ForeignKey(
        User,
        related_name='owner',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        models.UniqueConstraint(
            fields=['owner', 'recipe'],
            name='unique_recipe'
        )


class Favorite(models.Model):
    """Модель избранных рецептов пользователя."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reader',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='likerecipe',
        verbose_name='Рецепт'
    )

    class Meta:
        models.UniqueConstraint(
            fields=['reader', 'likerecipe'],
            name='unique_likerecipe'
        )


class Subscription(models.Model):
    """Модель для подписок на авторов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='publisher',
        verbose_name='Автор'
    )

    class Meta:
        models.UniqueConstraint(
            fields=['subscriber', 'publisher'],
            name='unique_subscription'
        )
