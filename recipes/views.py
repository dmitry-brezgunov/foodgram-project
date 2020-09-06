from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import FavoriteRecipes, Recipe, ShopList
from users.models import FollowAuthor


def index_page(request):
    recipe_list = Recipe.objects.select_related(
        'author').prefetch_related('tags').order_by('-pub_date').all()
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
         'favorites_list': favorites_list, 'shop_list': shop_list})


@login_required
def new_recipe(request):
    new_recipe = True
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('index')
    else:
        form = RecipeForm(files=request.FILES or None)
    shop_list = ShopList.objects.get_or_create(
        user=request.user)[0].recipes.all()
    return render(request, 'formRecipe.html', {
        'form': form, 'new_recipe': new_recipe, 'shop_list': shop_list})


def recipe_page(request, pk):
    recipe = get_object_or_404(Recipe.objects.select_related('author'), pk=pk)
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
            user=request.user)[0].recipes.filter(pk=pk)
        subscriptons_list = FollowAuthor.objects.get_or_create(
            user=request.user)[0].authors.all()
    return render(
        request, 'singlePage.html',
        {'recipe': recipe, 'ingredients': ingredients,
         'tags': tags, 'index': index, 'favorite': favorite,
         'shop_list': shop_list, 'subscriptons_list': subscriptons_list})


@login_required
def favorite(request):
    recipe_list = FavoriteRecipes.objects.get(
        user=request.user).recipes.prefetch_related(
            'tags').select_related('author').order_by('-pub_date').all()
    shop_list = ShopList.objects.get_or_create(
        user=request.user)[0].recipes.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    favorite_page = True
    return render(
        request, 'favorite.html',
        {'page': page, 'paginator': paginator, 'favorite_page': favorite_page,
         'shop_list': shop_list})


def shop_list_page(request):
    shop_list = ShopList.objects.get_or_create(
        user=request.user)[0].recipes.all()
    shop = True
    return render(
        request, 'shopList.html', {'shop_list': shop_list, 'shop': shop})
