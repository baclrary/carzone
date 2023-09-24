from django import template

register = template.Library()

@register.simple_tag
def is_active(request, pattern):
    if pattern == '/':
        return "active" if request.path == '/' else ""
    elif pattern in request.path:
        return "active"
    return ""


@register.filter
def beautiful_price(value):
    try:
        return '{:,.0f}'.format(value).replace(',', ' ')
    except:
        return value