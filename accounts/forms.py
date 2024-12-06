from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import CustomUser, JobPost, JobAlert, Feedback, Profile

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

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'requirements', 'location', 'salary', 'job_duration', 'job_type', 'budget']
        labels = {
            'title': 'Job Title',
            'description': 'Job Description',
            'requirements': 'Job Requirements',
            'location': 'Job Location',
            'salary': 'Salary/Budget',
            'job_duration': 'Job Duration',
            'job_type': 'Job Type',
            'budget': 'Budget (if applicable)',
        }
        widgets = {
            'job_type': forms.Select(choices=JobPost.JOB_TYPE_CHOICES),
        }

class JobSearchForm(forms.Form):
    title = forms.CharField(max_length=255, required=False)
    location = forms.CharField(max_length=255, required=False)
    min_salary = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_salary = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('search', 'Search'))

class JobAlertForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save Preferences'))

    class Meta:
        model = JobAlert
        fields = ['job_title', 'location', 'industry']

class CandidateSearchForm(forms.Form):
    qualifications = forms.CharField(max_length=255, required=False)
    skills = forms.CharField(max_length=255, required=False)
    location = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('search', 'Search'))

class NotificationPreferencesForm(forms.Form):
    immediate = forms.BooleanField(required=False)
    daily = forms.BooleanField(required=False)
    weekly = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save Preferences'))

class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Feedback
        fields = ['issue_type', 'description']

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
