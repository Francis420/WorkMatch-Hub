from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import JobPost, JobAlert

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 
                  'description', 
                  'requirements', 
                  'location', 
                  'salary', 
                  'job_duration', 
                  'job_type',
                  'total_slots',
                  'remaining_slots'
        ]
        labels = {
            'title': 'Job Title',
            'description': 'Job Description',
            'requirements': 'Job Requirements',
            'location': 'Job Location',
            'salary': 'Salary/Budget',
            'job_duration': 'Job Duration',
            'job_type': 'Job Type',
            'total_slots': 'Total Slots',
            'remaining_slots': 'Remaining Slots'
        }
        widgets = {
            'job_type': forms.Select(choices=JobPost.JOB_TYPE_CHOICES),
        }

class JobSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Job Title'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Location'})
    )
    min_salary = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Min Salary'})
    )
    max_salary = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Max Salary'})
    )

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
        fields = ['job_title', 
                  'job_description', 
                  'location'
        ]