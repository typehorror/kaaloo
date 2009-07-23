from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

from common.shortcuts import render_response, render_string
from project.forms import ProjectForm, NewProjectForm, ProjectSpectatorForm
from project.models import Project

@login_required
def project_list_view(request):
    context = {'current':'projects'}
    context['projects'] = Project.objects.for_user(request.user)
    return render_response(request, 'project/project_view.html', context)

@login_required
def project_detail_view(request,id):
    context = {'current':'projects'}
    user = request.user
    projects = Project.objects.for_user(request.user).filter(id=int(id))
    if not projects:
        raise Http404
    project = projects[0]
    if request.POST:
        form = ProjectForm(instance=project, data=request.POST)
        if form.is_valid():
            form.save()
            context['project_saved'] = True
        context['form'] = form
    else:
        context['form'] = ProjectForm(instance=project)
    context['spectator_form'] = ProjectSpectatorForm(instance=project, user=request.user)
    context['project'] = project
    return render_response(request, 'project/project_detail_view.html', context)

@login_required
def add_project_view(request):
    context = {'current':'projects'}
    if request.method == "POST":
        form = NewProjectForm(data=request.POST)
        if form.is_valid():
            project = form.save()
            project.owners = [request.user]
            project.save()
            return HttpResponseRedirect(reverse('project_detail_view', args=[project.id]))
        else:
            context['form'] = form
    else:
        context['form'] = NewProjectForm()
    return render_response(request, 'project/add_project.html', context)
