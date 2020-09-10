from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from recipes.models import FavoriteRecipes, Recipe, ShopList, Tag

from .forms import UserSignUpForm
from .models import FollowAuthor, User


class SignUp(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/singup.html'


class Login(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signin'] = True
        return context


class PasswordChange(PasswordChangeView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = ShopList.objects.get_or_create(
            user=self.request.user)[0].recipes.all()
        context['passwordchange'] = True
        return context


def author_page(request, username):
    author = get_object_or_404(User, username=username)

    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        recipes = Recipe.objects.filter(
            author=author, tags__slug__in=filters).distinct().select_related(
                'author').prefetch_related('tags').order_by('-pub_date')

    else:
        recipes = Recipe.objects.filter(
            author=author).select_related(
                'author').prefetch_related('tags').order_by('-pub_date')

    subscriptons_list = []
    shop_list = []
    favorites_list = []

    if request.user.is_authenticated:
        favorites_list = FavoriteRecipes.objects.get_or_create(
            user=request.user)[0].recipes.all()
        shop_list = ShopList.objects.get_or_create(
                user=request.user)[0].recipes.all()
        subscriptons_list = FollowAuthor.objects.get_or_create(
            user=request.user)[0].authors.all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    index = True
    tags = Tag.objects.all()

    return render(
        request, 'authorRecipe.html',
        {'profile': author, 'page': page,
         'paginator': paginator, 'index': index,
         'favorites_list': favorites_list, 'shop_list': shop_list,
         'tags': tags, 'subscriptions_list': subscriptons_list})


@login_required
def subscriptions_page(request):
    authors_list = FollowAuthor.objects.get_or_create(
        user=request.user)[0].authors.prefetch_related(
            'recipes').order_by('username')

    shop_list = ShopList.objects.get_or_create(
        user=request.user)[0].recipes.all()

    paginator = Paginator(authors_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    subscriptions = True

    return render(
        request, 'myFollow.html',
        {'page': page, 'paginator': paginator, 'subscriptions': subscriptions,
         'shop_list': shop_list})
