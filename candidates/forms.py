from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms

class CandidateSearchForm(forms.Form):
    qualifications = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Qualifications'})
    )
    skills = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Skills'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Location'})
    )