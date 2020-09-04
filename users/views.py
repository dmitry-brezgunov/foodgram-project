from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import UserSignUpForm
from .models import User, FollowAuthor
from recipes.models import Recipe


class SignUp(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/singup.html'


@login_required
def author_page(request, username):
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(
        author=author).select_related(
            'author').prefetch_related('tags').order_by('-pub_date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    index = True
    return render(
        request, 'authorRecipe.html',
        {'profile': author, 'page': page,
         'paginator': paginator, 'index': index})


@login_required
def subscriptions_page(request):
    authors_list = []
    if FollowAuthor.objects.filter(user=request.user).exists():
        authors_list = FollowAuthor.objects.get(
            user=request.user).authors.all()
    paginator = Paginator(authors_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    subscriptions = True
    return render(
        request, 'myFollow.html',
        {'page': page, 'paginator': paginator, 'subscriptions': subscriptions})
