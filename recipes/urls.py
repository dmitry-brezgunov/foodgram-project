from django.urls import path

from .views import (favorite, index_page, new_recipe, recipe_page,
                    shop_list_page, recipe_edit, recipe_delete)

urlpatterns = [
    path("", index_page, name="index"),
    path("recipe/new", new_recipe, name="new_recipe"),
    path("recipe/<int:recipe_id>", recipe_page, name="recipe_page"),
    path("favorite", favorite, name="favorite"),
    path("shop-list", shop_list_page, name="shop_list"),
    path("recipe/edit/<int:recipe_id>", recipe_edit, name="recipe_edit"),
    path("recipe/delete/<int:recipe_id>", recipe_delete, name="recipe_delete"),
]
