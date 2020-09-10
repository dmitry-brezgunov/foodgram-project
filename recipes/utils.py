from django.db.models import F, Sum


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient]
    return ingredients


def generate_shop_list_file(request, recipes):
    ingredient_list = recipes.annotate(
        name=F('ingredientamount__ingredient__title'),
        dimension=F('ingredientamount__ingredient__dimension')).values(
            'name', 'dimension').annotate(
                total=Sum('ingredientamount__amount')).order_by('name')

    with open(f'media/shop-lists/{request.user}.txt', 'w',
              encoding='utf-8') as f:

        for ingredient in ingredient_list:
            name = ingredient['name']
            dimension = ingredient['dimension']
            total = ingredient['total']
            f.write(f'{name} ({dimension}) - {total} \n')
