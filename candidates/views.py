from django.shortcuts import render, get_object_or_404
from .forms import CandidateSearchForm
from accounts.models import CustomUser 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

def candidate_profile(request, candidate_id):
    candidate = get_object_or_404(User, id=candidate_id)
    return render(request, 'candidates/candidate_profile.html', {'candidate': candidate})

def candidate_search(request):
    form = CandidateSearchForm(request.GET or None)
    candidates = CustomUser.objects.filter(is_job_seeker=True)

    if form.is_valid():
        if form.cleaned_data['qualifications']:
            candidates = candidates.filter(profile__qualifications__icontains=form.cleaned_data['qualifications'])
        if form.cleaned_data['skills']:
            candidates = candidates.filter(profile__skills__icontains=form.cleaned_data['skills'])
        if form.cleaned_data['location']:
            candidates = candidates.filter(profile__location__icontains=form.cleaned_data['location'])

    return render(request, 'candidates/candidate_search.html', {'form': form, 'candidates': candidates})