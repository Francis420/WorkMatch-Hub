from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .forms import CandidateSearchForm
from accounts.models import CustomUser
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
            candidates = candidates.filter(profile__education__icontains=form.cleaned_data['qualifications'])
        if form.cleaned_data['skills']:
            candidates = candidates.filter(profile__skills__icontains=form.cleaned_data['skills'])
        if form.cleaned_data['location']:
            candidates = candidates.filter(profile__location__icontains=form.cleaned_data['location'])

    paginator = Paginator(candidates, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'candidates/candidate_search.html', {'form': form, 'page_obj': page_obj})