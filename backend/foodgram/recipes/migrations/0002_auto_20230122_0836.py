# Generated by Django 2.2.28 on 2023-01-22 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeingredients',
            name='recipe',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipe', to='recipes.RecipeIngredients', verbose_name='Инградиент'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_favorited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_in_shopping_cart',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='ingredient',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='recipes.Ingredient'),
            preserve_default=False,
        ),
    ]
