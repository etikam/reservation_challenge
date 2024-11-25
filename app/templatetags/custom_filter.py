from django import template

register = template.Library()

@register.filter()
def price(value):
    try:
        value = float(value)
        return f"${value:.0f} GNF /Heure" 
    except (ValueError, TypeError):
        return "$0.00 GNF" 
    

