from django import template

from project.models import Project

register = template.Library()

@register.inclusion_tag('project_item.html')
def project_item(project, user):
    if project in Project.objects.for_user(user):
        read_only = False
    else:
        read_only = True
    return {'project': project, 'read_only': read_only}
