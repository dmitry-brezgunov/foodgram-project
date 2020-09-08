from django.db import models

from users.models import User


class Ingredient(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    dimension = models.CharField(
        max_length=50, verbose_name='Единицы измерения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    color = models.CharField(max_length=255, verbose_name='Цвет')
    slug = models.SlugField(unique=True, verbose_name='Уникальный адрес')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientAmount',
        related_name='recipes', verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги')
    cook_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления')
    slug = models.SlugField(
        unique=True, blank=True, null=True, verbose_name='Уникальный адрес')
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.ingredient} для {self.recipe}'

    class Meta:
        verbose_name = 'Кол-во ингредиента'
        verbose_name_plural = 'Кол-во ингредиентов'


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_recipes',
        verbose_name='Пользователь')
    recipes = models.ManyToManyField(
        Recipe, related_name='favorite_recipes', verbose_name='Рецепты',
        blank=True)

    def __str__(self):
        return f'Избранные рецепты {self.user}'

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShopList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shop_list',
        verbose_name='Пользователь')
    recipes = models.ManyToManyField(
        Recipe, related_name='shop_list', verbose_name='Рецепты', blank=True)

    def __str__(self):
        return f'Список покупок {self.user}'

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
