from django.urls import path

from .views import (favorite, index_page, new_recipe, recipe_page,
                    shop_list_page)

urlpatterns = [
    path("", index_page, name="index"),
    path("recipe/new", new_recipe, name="new_recipe"),
    path("recipe/<int:pk>", recipe_page, name="recipe_page"),
    path("favorite", favorite, name='favorite'),
    path("shop-list", shop_list_page, name='shop_list'),
]
