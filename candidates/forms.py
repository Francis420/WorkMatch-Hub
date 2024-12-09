from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CandidateSearchForm(forms.Form):
    qualifications = forms.CharField(max_length=255, required=False)
    skills = forms.CharField(max_length=255, required=False)
    location = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('search', 'Search'))