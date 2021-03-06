from django.urls import path

from .views import (FavoritesView, IngredientsViews, PurchasesView,
                    SubscriptionsView)

urlpatterns = [
    path("favorites/", FavoritesView.as_view(), name='add_favorites'),
    path("favorites/<int:recipe_id>/", FavoritesView.as_view(),
         name='delete_favorites'),
    path("purchases/", PurchasesView.as_view(), name='add_purchase'),
    path("purchases/<int:recipe_id>/", PurchasesView.as_view(),
         name='delete_purchase'),
    path("subscriptions/", SubscriptionsView.as_view(),
         name='add_subscription'),
    path("subscriptions/<int:author_id>/", SubscriptionsView.as_view(),
         name='delete_subscription'),
    path("ingredients/", IngredientsViews.as_view(), name='get_ingredients'),
]
