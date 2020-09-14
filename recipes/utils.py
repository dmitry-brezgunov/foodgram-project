from users.models import FollowAuthor

from .models import FavoriteRecipes


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]

            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient]

    return ingredients


def get_favorites_list(request):
    favorites_list = []
    if request.user.is_authenticated:

        favorites_list = FavoriteRecipes.objects.get_or_create(
            user=request.user
        )[0].recipes.all()

    return favorites_list


def get_subscriptons_list(request):
    subscriptons_list = []
    if request.user.is_authenticated:

        subscriptons_list = FollowAuthor.objects.get_or_create(
            user=request.user
        )[0].authors.all()

    return subscriptons_list
