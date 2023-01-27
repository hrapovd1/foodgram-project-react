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
            fields=['user', 'author'],
            name='unique_subscription'
        )


class Ingredient(models.Model):
    """Модель для инградиентов."""
    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(max_length=30)


class RecipeIngredients(models.Model):
    """Модель связи рецепта с инградиентами."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.DO_NOTHING
    )
    amount = models.PositiveSmallIntegerField()


class Tag(models.Model):
    """Модель для тегов."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=10)


class Recipe(models.Model):
    """Модель рецептов."""
    tags = models.ManyToManyField(
        Tag,
        related_name='tags'
    )
    author = models.ForeignKey(
        User,
        related_name='author',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        RecipeIngredients,
        related_name='recipe',
        verbose_name='Инградиент'
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
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в мин.',
        help_text='Заполните время приготовления'
    )

    class Meta:
        ordering = ['id']


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
        related_name='shoppingcart',
        verbose_name='Рецепт'
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_shopping_cart'
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
        related_name='favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite'
        )
