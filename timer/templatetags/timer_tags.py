from django import template

register = template.Library()

@register.inclusion_tag('timer_item.html')
def timer_item(time_record):
    return {'time_record':time_record}
