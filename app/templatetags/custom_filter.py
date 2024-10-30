from django import template

register = template.Library()

@register.filter()
def price(value):
    try:
        value = float(value)
        return f"${value:.0f} GNF /Heure" 
    except (ValueError, TypeError):
        # s'il n'arrive pas à convertir la valeur du prix passé en argument du filtre, 
        # ce que le prix n'est probablement pas un prix valiide; donc je l'annule
        return "$0.00 GNF" 
