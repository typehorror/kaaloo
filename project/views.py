from django.contrib.auth.decorators import login_required
# favour django-mailer but fall back to django.core.mail
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

from common.shortcuts import render_response, render_string
from project.forms import ProjectForm

def project_view(request):
    context = {}
    context['projects'] = request.user.projects.all()
    if request.method == "POST":
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            context['project'] = form.save()
            return render_response(request, 'project/project_created.html', context)
        else:
            context['project_form'] = form
    else:
        context['project_form'] = ProjectForm()

    return render_response(request, 'project/project_view.html', context)
