import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from recipes.models import FavoriteRecipes, Ingredient, Recipe, ShopList
from users.models import FollowAuthor, User


class FavoritesView(View, LoginRequiredMixin):
    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        user_favorites = FavoriteRecipes.objects.get_or_create(
            user=request.user)

        user_favorites[0].recipes.add(recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user_favorites = get_object_or_404(FavoriteRecipes, user=request.user)
        user_favorites.recipes.remove(recipe)
        return JsonResponse({'success': True})


class PurchasesView(View, LoginRequiredMixin):
    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        user_shop_list = ShopList.objects.get_or_create(
            user=request.user)

        user_shop_list[0].recipes.add(recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user_shop_list = get_object_or_404(ShopList, user=request.user)
        user_shop_list.recipes.remove(recipe)
        return JsonResponse({'success': True})


class SubscriptionsView(View, LoginRequiredMixin):
    def post(self, request):
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, pk=author_id)

        if author == request.user:
            return JsonResponse({'success': False})

        user_subscriptions = FollowAuthor.objects.get_or_create(
            user=request.user)

        user_subscriptions[0].authors.add(author)
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        author = get_object_or_404(User, pk=author_id)
        user_subscriptions = get_object_or_404(FollowAuthor, user=request.user)
        user_subscriptions.authors.remove(author)
        return JsonResponse({'success': True})


class IngredientsViews(View, LoginRequiredMixin):
    def get(self, request):
        query = self.request.GET['query']

        ingredients_list = Ingredient.objects.filter(
            title__istartswith=query
        ).values(
            'title', 'dimension'
        ).order_by()

        return JsonResponse(list(ingredients_list), safe=False)
