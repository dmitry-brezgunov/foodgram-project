from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    '''Фильтр для добавления класса к полю в шаблоне'''
    return field.as_widget(attrs={"class": css})


@register.filter
def format_count(word, count):
    '''Фильтр для склонение слова 'рецепт' по числу'''
    count -= 3
    remainder_ten = count % 10
    remainder_hundred = count % 100
    if remainder_ten == 0:
        word += 'ов'
    elif remainder_ten == 1 and remainder_hundred != 11:
        word += ''
    elif remainder_ten < 5 and remainder_hundred not in [11, 12, 13, 14]:
        word += 'а'
    else:
        word += 'ов'
    return word


@register.filter
def get_filter_values(value):
    return value.getlist('filters')


@register.filter
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.slug in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.slug)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.slug)

    return new_request.urlencode()


@register.simple_tag
def url_replace(request, field, value):
    params = request.GET.copy()
    params[field] = value
    return params.urlencode()
