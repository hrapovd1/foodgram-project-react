# Generated by Django 2.2.28 on 2023-01-25 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20230125_1840'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['id']},
        ),
    ]