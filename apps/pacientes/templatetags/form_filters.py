from django import template

register = template.Library()

@register.filter
def get_field_display(form, field_name):
    """Devuelve el verbose_name del campo del formulario."""
    try:
        return form.fields[field_name].label or field_name
    except (KeyError, AttributeError):
        return field_name