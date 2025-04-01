from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import JobPost, JobAlert

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            'title', 
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
            'job_type': forms.Select(choices=JobPost.JOB_TYPE_CHOICES, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'job_duration': forms.TextInput(attrs={'class': 'form-control'}),
            'total_slots': forms.NumberInput(attrs={'class': 'form-control'}),
            'remaining_slots': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('update', 'Update Job', css_class='btn btn-success btn-lg'))

class JobSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Job Title', 'class': 'form-control'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Location', 'class': 'form-control'})
    )
    min_salary = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Min Salary', 'class': 'form-control'})
    )
    max_salary = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Max Salary', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('search', 'Search', css_class='btn btn-primary btn-block'))

class JobAlertForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save Preferences', css_class='btn btn-primary btn-lg'))

    class Meta:
        model = JobAlert
        fields = ['job_title', 'job_description', 'location']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'job_description': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'})
        }
