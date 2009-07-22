from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.hashcompat import sha_constructor

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# favour django-mailer but fall back to django.core.mail
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail


from common.shortcuts import render_response, render_string
from contact.forms import AddContactForm
from contact.models import ContactRequest, InviteRequest
from profile.forms import SetPasswordForm
from profile.models import Profile

@login_required
def contact_view(request):
    context = {'current':'contacts',
               'contacts': request.user.get_profile().contacts.all()}
    return render_response(request, 'contact/contact.html', context)
    
def contact_requests_view(request):
    """
    show a list of request
    """
    context = {'current':'contacts',
               'contact_requests': request.user.contact_requests_received.all() }
    return render_response(request, 'contact/contact_requests.html', context)
    
@login_required
def contact_added(request):
    """
    view used for google analytics goals 
    """
    context = {'current':'contacts'}
    return render_response(request, 'contact/contact_confirm_added.html', context)

@login_required
def contact_refused(request):
    """
    view used for google analytics goals 
    """
    context = {'current':'contacts'}
    return render_response(request, 'contact/contact_confirm_refused.html', context)

@login_required
def contact_confirm_view(request, key):
    """
    
    """
    context = {'current':'contacts'}
    contact_request = get_object_or_404(ContactRequest, key=key, to_user=request.user)
    context ['contact_request'] = contact_request
    if request.method == 'POST':
        if request.POST.has_key('add_contact'):
            request.user.get_profile().contacts.add(contact_request.from_user.get_profile())
            contact_request.delete()
            return HttpResponseRedirect(reverse('contact_added'))
        elif request.POST.has_key('refuse_contact'):
            contact_request.delete()
            return HttpResponseRedirect(reverse('contact_refused'))
        else:
            return HttpResponseRedirect(reverse('profile.views.profile_view'))
    
    return render_response(request, 'contact/contact_confirm.html', context)
    
def invite_confirm_view(request, key):
    """
    Create an account for the user.
    """
    """
    Account creation from email link.
    """
    invites = InviteRequest.objects.filter(key=key)

    if not invites:
        return HttpResponseRedirect(reverse('login_view'))

    invite = invites[0]

    # check that user does not already exist with this email
    if User.objects.filter(email__iexact=invite.to_email):
        return HttpResponseRedirect(reverse('login_view'))

    context = {}
    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password2']
            user = User.objects.create_user(sha_constructor(str(invite.to_email)).hexdigest()[:30], invite.to_email, password)
            profile = Profile.objects.create(user=user)
            user = authenticate(username=user.username, password=password)
            login(request, user)
            context['email_to'] = user.email
            context['password'] = password
            text_content = render_string(request,
                                         'email/welcome.txt',
                                         context)
            send_mail('Welcome to kaaloo',
                      text_content,
                      settings.DEFAULT_EMAIL_FROM,
                      [user.email, ])
            
            # transform all invites in friend request
            invites = InviteRequest.objects.filter(to_email__iexact = user.email)
            for invite in invites:
                ContactRequest.objects.create(from_user=invite.from_user, to_user=user)
            invites.delete()
            return HttpResponseRedirect(reverse('contact_requests_view'))
        else:
            context['password_form'] = form
    else:
        context['password_form'] = SetPasswordForm()
    return render_response(request, 'profile/create_account.html', context)
    
@login_required
def invite_sent(request):
    context = {'current':'contacts'}
    return render_response(request, 'contact/contact_invite_sent.html', context)

@login_required
def add_contact_view(request):
    context = {'current':'contacts'}
    if request.method == 'POST':
        form = AddContactForm(data=request.POST)
        if form.is_valid():
            mail_context = {'from_user': request.user }
            email = form.cleaned_data['email']
            email_owners = User.objects.filter(email__iexact=email)
            if email_owners:
                email_owner = email_owners[0]
                if email_owner == request.user:
                    context['message'] = 'The email address you entered is yours. It\'s may seam rude but you cannot invite yourself to be a contact.'
                    return render_response(request, 'contact/request_already_sent.html', context)
                contact_requests = ContactRequest.objects.filter(from_user=request.user,
                                                                 to_user=email_owner)
                # make sure to not double an existing request:
                if contact_requests:
                    context['message'] = 'You already create a request to this person. We recommand you to contact directly this person. '
                    return render_response(request, 'contact/request_already_sent.html', context)
                if email_owner in request.user.get_profile().contacts.all():
                    context['message'] = 'You are already friend with this person'
                    return render_response(request, 'contact/request_already_sent.html', context)
                contact_request = ContactRequest(from_user=request.user, to_user=email_owner)
                mail_context['email_to'] = email
                mail_context['to_user'] = email_owner
                mail_context['contact_request'] = contact_request
                text_content = render_string(request,
                                            'email/contact_request.txt',
                                             mail_context)
                send_mail('Contact Request',
                           text_content,
                           settings.DEFAULT_EMAIL_FROM,
                           [email_owner.email, ])
                contact_request.save()
            else:
                invite_requests = InviteRequest.objects.filter(from_user=request.user, 
                                                               to_email__iexact=email)
                # make sure to not double an existing request:
                if invite_requests:
                    context['message'] = 'You already create a request to this person. We recommand you to contact directly this person. '
                    return render_response(request, 'contact/request_already_sent.html', context)
                
                invite_request = InviteRequest(from_user=request.user,
                                               to_email=email)
                mail_context['email_to'] = email
                mail_context['invite_request'] = invite_request
                mail_context['other_requests'] = InviteRequest.objects.filter(to_email__iexact=email)
                text_content = render_string(request,
                                            'email/invite.txt',
                                             mail_context)
                send_mail('Someone invited you to join Kaaloo',
                           text_content,
                           settings.DEFAULT_EMAIL_FROM,
                           [email, ])
                invite_request.save()
            return HttpResponseRedirect(reverse('invite_sent'))
        else:
            context['contact_form'] = form
    else:
        context['contact_form'] = AddContactForm()
    return render_response(request, 'contact/add_contact.html', context)
