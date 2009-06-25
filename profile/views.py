from django.utils.hashcompat import sha_constructor
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, RequestSite

# favour django-mailer but fall back to django.core.mail
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail


from profile.forms import LoginForm, RegisterForm, ProfileForm, UserForm, SetPasswordForm
from common.shortcuts import render_response, render_string
from profile.models import Profile, Registration

def login_view(request, template_name='profile/login.html',redirect_field_name=REDIRECT_FIELD_NAME):
    context = {}
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = LoginForm(request)
    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return render_response(request,template_name, {
        'login_form': form,
        'register_form': RegisterForm(),
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    })
login_view = never_cache(login_view)


def register_confirm(request, key):
    """
    Account creation from email link.
    """
    registration = Registration.objects.filter(key=key)

    if not registration:
        return HttpResponseRedirect(reverse('login_view'))

    registration = registration[0]

    # check that user does not already exist with this email
    if User.objects.filter(email__iexact=registration.email):
        Registration.objects.filter(email__iexact=registration.email).delete()
        return HttpResponseRedirect(reverse('login_view'))
    context = {'registration': registration}
    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password2']
            user = User.objects.create_user(sha_constructor(str(registration.email)).hexdigest()[:30], registration.email, password)
            profile = Profile.objects.create(user=user)
            user = authenticate(username=user.username, password=password)
            login(request, user)
            context['email_to'] = registration.email
            context['password'] = password
            text_content = render_string(request,
                                         'email/welcome.txt',
                                         context)
            send_mail('Welcome to kaaloo',
                      text_content,
                      settings.DEFAULT_EMAIL_FROM,
                      [user.email, ])
            Registration.objects.filter(email__iexact=registration.email).delete()
            return HttpResponseRedirect(reverse('profile_view'))
        else:
            context['password_form'] = form
    else:
        context['password_form'] = SetPasswordForm()

    return render_response(request, 'profile/create_account.html', context)
    

def register_view(request):
    """
    Formular which send registration email to user
    """
    context = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            registration = form.save()
            context['registration'] = registration
            context['email_to'] = registration.email
            text_content = render_string(request,
                                         'email/registration.txt',
                                         context)
            send_mail('Registration to kaaloo',
                      text_content,
                      settings.DEFAULT_EMAIL_FROM,
                      [registration.email, ])
            return render_response(request, 'profile/reg_email_sent.html', context)
        else:
            # form is invalid
            context['register_form'] = form
    else:
        # no post, user just arrived
        context['register_form'] = RegisterForm()
    context['login_form'] = LoginForm()
    return render_response(request, 'profile/login.html', context)


@login_required
def profile_view(request):
    """
    Allow user to add personnal data to his profile
    """
    profile = request.user.get_profile()
    context = {}
    if request.method == "POST":
        profile_form = ProfileForm(instance=profile, data=request.POST)
        user_form = UserForm(instance=request.user, data=request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            context['profile_saved'] = True
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    context.update({'user_form': user_form,
                    'profile_form': profile_form,
                    'current':'account'})
    return render_response(request, 'profile/profile.html', context)

@login_required
def password_view(request):
    """
    Allow user to change his password by entering his old one
    """
    profile = request.user.get_profile()
    context = {}
    if request.method == "POST":
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            context['password_saved'] = True
    else:
        password_form =PasswordChangeForm(user=request.user)
    context.update({'password_form': password_form,
                    'current':'account'})
    return render_response(request, 'profile/password.html', context)
password_view = never_cache(password_view)
    
@login_required
def logout_view(request):
    """
    disconnect the current user.
    """
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse('profile.views.login_view'))
