from django import template

register = template.Library()

@register.filter
def vnd(value):
    try:
        return "{:,.0f} VND".format(value).replace(",", ".")
    except:
        return value