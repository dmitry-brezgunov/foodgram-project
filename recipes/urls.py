from django.urls import path

from .views import index_page, new_recipe, recipe_page, favorite

urlpatterns = [
    path("", index_page, name="index"),
    path("recipe/new", new_recipe, name="new_recipe"),
    path("recipe/<int:pk>", recipe_page, name="recipe_page"),
    path("favorite", favorite, name='favorite')
]
