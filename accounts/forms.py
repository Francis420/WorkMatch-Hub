from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import CustomUser, Profile

class JobSeekerSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class EmployerSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class NotificationPreferencesForm(forms.Form):
    immediate = forms.BooleanField(required=False)
    daily = forms.BooleanField(required=False)
    weekly = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save Preferences'))

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'profile_picture', 'skills', 'experience', 'education',
            'resume', 'location', 'job_preferences', 'availability', 'contact_number', 'facebook_link'
        ]

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'employer_name', 'company_logo', 'company_description', 'industry',
            'website', 'contact_person', 'contact_number', 'facebook_link'
        ]

class AdminCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_staff', 'is_superuser')