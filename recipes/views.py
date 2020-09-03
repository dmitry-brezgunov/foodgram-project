from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import Recipe, FavoriteRecipes
from .forms import RecipeForm


def index_page(request):
    recipe_list = Recipe.objects.select_related(
        'author').prefetch_related('tags').order_by('-pub_date').all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    index = True
    return render(
        request, "index.html",
        {'page': page, 'paginator': paginator, 'index': index})


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
        form = RecipeForm()
    return render(
        request, 'formRecipe.html', {'form': form, 'new_recipe': new_recipe})


def recipe_page(request, pk):
    recipe = get_object_or_404(Recipe.objects.select_related('author'), pk=pk)
    ingredients = recipe.ingredientamount_set.all()
    tags = recipe.tags.all()
    return render(
        request, 'singlePage.html',
        {'recipe': recipe, 'ingredients': ingredients, 'tags': tags})


@login_required
def favorite(request):
    recipe_list = []
    if FavoriteRecipes.objects.filter(user=request.user).exists():
        recipe_list = FavoriteRecipes.objects.get(
            user=request.user).recipes.prefetch_related(
                'tags').select_related('author').order_by('-pub_date').all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    favorite = True
    return render(
        request, 'favorite.html',
        {'page': page, 'paginator': paginator, 'favorite': favorite})
