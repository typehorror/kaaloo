from django.template import RequestContext
from django.template.loader import render_to_string

def render_response(req, *args, **kwargs):
    """
    Helper method which passes RequestContext to templates instead of plain Context.
    Passes some additional variables to templates
    """
    from django.shortcuts import render_to_response
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)


def render_string(req, *args, **kwargs):
    """
    Helper method which passes RequestContext to templates instead of plain Context.
    Passes some additional variables to templates
    """
    from django.template.loader import render_to_string
    kwargs['context_instance'] = RequestContext(req)
    return render_to_string(*args, **kwargs)

