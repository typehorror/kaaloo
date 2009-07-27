from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.db.models import Q

from common.shortcuts import render_response, render_string
from project.forms import ProjectForm, NewProjectForm, ProjectSpectatorForm
from project.models import Project

@login_required
def project_list_view(request):
    context = {'current':'projects',
               'content_title': _('All projects')}
    context['projects'] = Project.objects.for_user(request.user)
    return render_response(request, 'project/project_view.html', context)

@login_required
def project_detail_view(request,id):
    context = {'current':'projects'}
    user = request.user
    project = Project.objects.get_for_user(user=request.user, id=int(id))

    if request.POST:
        form = ProjectForm(instance=project, data=request.POST)
        if form.is_valid():
            form.save()
            context['project_saved'] = True
        context['form'] = form
    else:
        context['form'] = ProjectForm(instance=project)

    context['project'] = project
    context['spectators'] = project.spectators.all().select_related()
    context['owners'] = project.owners.all().select_related()
    context['collaborators'] = project.collaborators.all().select_related()
    context['new_spectators'] = User.objects.filter(profile__contacts__user=request.user).exclude(projects_as_spectator = project).select_related()
    context['new_collaborators'] = User.objects.filter(profile__contacts__user=request.user).exclude(projects_as_collaborator = project).select_related()
    context['new_owners'] = User.objects.filter(profile__contacts__user=request.user).exclude(owned_projects = project).select_related()

    return render_response(request, 'project/project_detail_view.html', context)

@login_required
def owner_form(request, project_id):
    project = Project.objects.write_access(user=request.user, id=int(project_id))
    context = {'project': project}
    context['owners'] = project.owners.all().select_related()
    context['new_owners'] = User.objects.filter(profile__contacts__user=request.user).exclude(owned_projects = project).select_related()
    return render_response(request, 'project/owner_form.html', context)


@login_required
def spectator_form(request, project_id):
    project = Project.objects.write_access(user=request.user, id=int(project_id))
    context = {'project': project}
    context['spectators'] = project.spectators.all().select_related()
    context['new_spectators'] = User.objects.filter(profile__contacts__user=request.user).exclude(projects_as_spectator = project).select_related()
    return render_response(request, 'project/spectator_form.html', context)


@login_required
def collaborator_form(request, project_id):
    project = Project.objects.write_access(user=request.user, id=int(project_id))
    context = {'project': project}
    context['collaborators'] = project.collaborators.all().select_related()
    context['new_collaborators'] = User.objects.filter(profile__contacts__user=request.user).exclude(projects_as_collaborator = project).select_related()
    return render_response(request, 'project/collaborator_form.html', context)


@login_required
def add_remove_spectator(request, project_id):
    project = Project.objects.write_access(user=request.user, id=int(project_id))
    if request.POST:
        already_spectators = request.POST.getlist('already_spectators')
        spectators = request.POST.getlist('spectators')
        users = list(User.objects.values_list('id', flat=True).filter(Q(projects_as_spectator=project,id__in=already_spectators)|Q(profile__contacts__user=request.user, id__in=spectators)|Q(profile__contacts__user=request.user, id__in=already_spectators)).distinct())
        project.spectators = users
        project.save()
    return render_to_response('project/user_list.html', {'user_objects': project.spectators.all()})

@login_required
def add_remove_owner(request, project_id):
    project = Project.objects.get(creator=request.user, id=int(project_id))
    if request.POST:
        already_owners = request.POST.getlist('already_owners')
        owners = request.POST.getlist('owners')
        users = list(User.objects.values_list('id', flat=True).filter(Q(owned_projects=project,id__in=already_owners)|Q(profile__contacts__user=request.user, id__in=owners)|Q(profile__contacts__user=request.user, id__in=already_owners)).distinct())
        project.owners = users
        project.save()
    return render_to_response('project/user_list.html', {'user_objects': project.owners.all()})

@login_required
def add_remove_collaborator(request, project_id):
    project = Project.objects.write_access(user=request.user, id=int(project_id))
    if request.POST:
        already_collaborators = request.POST.getlist('already_collaborators')
        collaborators = request.POST.getlist('collaborators')
        users = list(User.objects.values_list('id', flat=True).filter(Q(projects_as_collaborator=project,id__in=already_collaborators)|Q(profile__contacts__user=request.user, id__in=collaborators)|Q(profile__contacts__user=request.user, id__in=already_collaborators)).distinct())
        project.collaborators = users
        project.save()
    return render_to_response('project/user_list.html', {'user_objects': project.collaborators.all()})

@login_required
def add_project_view(request):
    context = {'current':'projects'}
    if request.method == "POST":
        form = NewProjectForm(data=request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            project.owners = [request.user]
            return HttpResponseRedirect(reverse('project_detail_view', args=[project.id]))
        else:
            context['form'] = form
    else:
        context['form'] = NewProjectForm()
    return render_response(request, 'project/add_project.html', context)

def my_projects_list_view(request):
    context = {'current':'projects',
               'content_title': _('Your projects')}
    context['projects'] = Project.objects.filter(owners=request.user)
    return render_response(request, 'project/project_view.html', context)
