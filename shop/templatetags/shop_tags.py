from django import template
from ..models import Color, Size

register = template.Library()


def create_path(path: dict):
    base = path.get('default')
    result = f'{base}'
    for key, value in path.items():
        if key == 'default':
            continue
        elif '?' not in result:
            result += f'?{key}={value}'
        else:
            result += f'&{key}={value}'
    return result


@register.filter()
def get_sort(path, param):
    path['sort'] = param
    return create_path(path)


@register.filter()
def get_page(path, param):
    path['page'] = param
    return create_path(path)


@register.simple_tag()
def get_sizes_clothes():
    sizes = Size.objects.filter(catalog__name='clothes')
    return sizes


@register.simple_tag()
def get_sizes_shoes():
    sizes = Size.objects.filter(catalog__name='shoes')
    return sizes


@register.simple_tag()
def get_colors():
    return Color.objects.all()
