# Generated by Django 3.1 on 2020-09-05 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_shoplist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriterecipes',
            name='recipes',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorite_recipes', to='recipes.Recipe', verbose_name='Рецепты'),
        ),
        migrations.AlterField(
            model_name='shoplist',
            name='recipes',
            field=models.ManyToManyField(blank=True, null=True, related_name='shop_list', to='recipes.Recipe', verbose_name='Рецепты'),
        ),
    ]
