from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from profile.models import Profile

class RegisterForm(forms.Form):
    register_email = forms.EmailField(max_length=128, label='Email')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
                  
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth',
                  'phone',
                  'cellular',
                  'address1',
                  'address2',
                  'city',
                  'zip_code',
                  'country',
                  'state',)

class LoginForm(forms.Form):
    """
    Review of the base class for authenticating users but using email instead.
    """
    email = forms.EmailField(max_length=128, label='Email')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label='Password' )

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            username = User.objects.get(email=email).username
        except:
            username = None
            raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


