from django.contrib import admin

from .models import FavoriteRecipes, Ingredient, IngredientAmount, Recipe, Tag, ShopList


class IngredientAmountInLine(admin.TabularInline):
    model = IngredientAmount
    extra = 1


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', )


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'cook_time', )
    search_fields = ('author', 'title', )
    list_filter = ('tags', )
    inlines = (IngredientAmountInLine, )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension', )
    search_fields = ('title', )


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount', )
    search_fields = ('ingredient', 'recipe', )


class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )


class ShopListAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(FavoriteRecipes, FavoriteRecipesAdmin)
admin.site.register(ShopList, ShopListAdmin)
