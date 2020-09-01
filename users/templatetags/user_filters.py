from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    '''Фильтр для добавления класса к полю в шаблоне'''
    return field.as_widget(attrs={"class": css})