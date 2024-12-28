from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica o valor pelo argumento fornecido"""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0  # Retorna 0 se não for possível realizar a multiplicação
