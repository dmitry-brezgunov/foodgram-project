from django.contrib import admin

from .models import (FavoriteRecipes, Ingredient, IngredientAmount, Recipe,
                     ShopList, Tag)


class IngredientAmountInLine(admin.TabularInline):
    model = IngredientAmount
    extra = 1
    autocomplete_fields = ('ingredient', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'color', 'slug', )
    search_fields = ('title', )


class RecipeAdmin(admin.ModelAdmin):
    def favorites_count(self, obj):
        return obj.favorite_recipes.count()

    favorites_count.short_description = 'Кол-во добавлений в Избранное'

    list_display = ('title', 'author', 'pub_date', )
    search_fields = ('title', )
    filter_horizontal = ('tags', )
    list_filter = ('tags', 'pub_date', 'author', )
    autocomplete_fields = ('ingredients', )
    inlines = (IngredientAmountInLine, )
    readonly_fields = ('favorites_count', )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension', )
    search_fields = ('title', )


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount', )
    search_fields = ('ingredient', 'recipe', )


class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )
    filter_horizontal = ('recipes', )


class ShopListAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )
    filter_horizontal = ('recipes', )


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(FavoriteRecipes, FavoriteRecipesAdmin)
admin.site.register(ShopList, ShopListAdmin)
