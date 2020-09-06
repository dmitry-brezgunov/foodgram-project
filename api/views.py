import json
from django.views.generic import View
from django.http import JsonResponse

from recipes.models import FavoriteRecipes, Recipe, ShopList
from users.models import FollowAuthor, User


class FavoritesView(View):
    def post(self, request):
        recipe_id = json.loads(request.body)['id']
        recipe = Recipe.objects.get(pk=recipe_id)
        user_favorites = FavoriteRecipes.objects.get_or_create(
            user=request.user)
        user_favorites[0].recipes.add(recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        user_favorites = FavoriteRecipes.objects.get(user=request.user)
        user_favorites.recipes.remove(recipe)
        return JsonResponse({'success': True})


class PurchasesView(View):
    def post(self, request):
        recipe_id = json.loads(request.body)['id']
        recipe = Recipe.objects.get(pk=recipe_id)
        user_shop_list = ShopList.objects.get_or_create(
            user=request.user)
        user_shop_list[0].recipes.add(recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        user_shop_list = ShopList.objects.get(user=request.user)
        user_shop_list.recipes.remove(recipe)
        return JsonResponse({'success': True})


class SubscriptionsView(View):
    def post(self, request):
        author_id = json.loads(request.body)['id']
        author = User.objects.get(pk=author_id)
        if author == request.user:
            return JsonResponse({'success': False})
        user_subscriptions = FollowAuthor.objects.get_or_create(
            user=request.user)
        user_subscriptions[0].authors.add(author)
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        author = User.objects.get(pk=author_id)
        user_subscriptions = FollowAuthor.objects.get(user=request.user)
        user_subscriptions.authors.remove(author)
        return JsonResponse({'success': True})