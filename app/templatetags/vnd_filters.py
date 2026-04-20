from django import template

register = template.Library()

@register.filter
def vnd(value):
    """Format số tiền VNĐ: 1500000 → 1.500.000 ₫"""
    try:
        amount = int(float(value))
        formatted = f"{amount:,}".replace(",", ".")
        return f"{formatted} ₫"
    except (ValueError, TypeError):
        return value
