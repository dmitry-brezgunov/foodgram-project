from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from users.models import FollowAuthor

from .forms import RecipeForm
from .models import (FavoriteRecipes, Ingredient, IngredientAmount, Recipe,
                     ShopList, Tag)
from .utils import get_ingredients


def index_page(request):
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        recipe_list = Recipe.objects.filter(
            tags__slug__in=filters).distinct().order_by(
                '-pub_date').select_related('author').prefetch_related('tags')
    else:
        recipe_list = Recipe.objects.select_related(
            'author').prefetch_related('tags').order_by('-pub_date').all()

    tags = Tag.objects.all()
    favorites_list = []
    shop_list = []

    if request.user.is_authenticated:
        favorites_list = FavoriteRecipes.objects.get_or_create(
            user=request.user)[0].recipes.all()
        shop_list = ShopList.objects.get_or_create(
            user=request.user)[0].recipes.all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    index = True

    return render(
        request, "index.html",
        {'page': page, 'paginator': paginator, 'index': index,
         'favorites_list': favorites_list, 'shop_list': shop_list,
         'tags': tags})


@login_required
def new_recipe(request):
    new_recipe = True

    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            ingredients = get_ingredients(request)

            for title, amount in ingredients.items():
                ingredient = Ingredient.objects.get(title=title)
                amount = IngredientAmount(
                    amount=amount, ingredient=ingredient, recipe=recipe)
                amount.save()
            form.save_m2m()
            return redirect('recipe_page', recipe_id=recipe.id)

    else:
        form = RecipeForm(files=request.FILES or None)
    shop_list = ShopList.objects.get_or_create(
        user=request.user)[0].recipes.all()

    return render(request, 'formRecipe.html', {
        'form': form, 'new_recipe': new_recipe, 'shop_list': shop_list})


def recipe_page(request, recipe_id):
    recipe = get_object_or_404(
        Recipe.objects.select_related('author').prefetch_related(
            'ingredientamount_set__ingredient'), pk=recipe_id)

    ingredients = recipe.ingredientamount_set.all()
    tags = recipe.tags.all()
    index = True
    subscriptons_list = []
    shop_list = []
    favorite = []

    if request.user.is_authenticated:
        shop_list = ShopList.objects.get_or_create(
            user=request.user)[0].recipes.all()
        favorite = FavoriteRecipes.objects.get_or_create(
            user=request.user)[0].recipes.filter(pk=recipe_id)
        subscriptons_list = FollowAuthor.objects.get_or_create(
            user=request.user)[0].authors.all()

    return render(
        request, 'singlePage.html',
        {'recipe': recipe, 'ingredients': ingredients,
         'tags': tags, 'index': index, 'favorite': favorite,
         'shop_list': shop_list, 'subscriptons_list': subscriptons_list})


@login_required
def favorite(request):
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        recipe_list = FavoriteRecipes.objects.get(
            user=request.user).recipes.filter(
                tags__slug__in=filters).distinct().prefetch_related(
                'tags').select_related('author').order_by('-pub_date').all()

    else:
        recipe_list = FavoriteRecipes.objects.get(
            user=request.user).recipes.all()

    shop_list = ShopList.objects.get_or_create(
        user=request.user)[0].recipes.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    favorite_page = True
    tags = Tag.objects.all()

    return render(
        request, 'favorite.html',
        {'page': page, 'paginator': paginator, 'favorite_page': favorite_page,
         'shop_list': shop_list, 'tags': tags})


def shop_list_page(request):
    shop_list = ShopList.objects.get_or_create(
        user=request.user)[0].recipes.all()
    shop = True
    return render(
        request, 'shopList.html', {'shop_list': shop_list, 'shop': shop})


@login_required
def recipe_edit(request, recipe_id):
    new_recipe = True
    edit = True
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related('tags'), pk=recipe_id)

    if request.user != recipe.author:
        return redirect('recipe_page', recipe_id=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILE, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_page', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)

    shop_list = ShopList.objects.get_or_create(
        user=request.user)[0].recipes.all()
    return render(
        request, 'formRecipe.html',
        {'form': form, 'new_recipe': new_recipe, 'shop_list': shop_list,
         'edit': edit})


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('index')
    return redirect('recipe_page', recipe_id=recipe_id)
