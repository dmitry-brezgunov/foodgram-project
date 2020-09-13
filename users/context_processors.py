from recipes.models import ShopList


def get_shop_list(request):
    shop_list = []
    if request.user.is_authenticated:
        shop_list = ShopList.objects.get_or_create(
                        user=request.user
                    )[0].recipes.all()
    return {'shop_list': shop_list}
