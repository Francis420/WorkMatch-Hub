from django.urls import path
from . import views

urlpatterns = [
    path('candidate/<int:candidate_id>/', views.candidate_profile, name='candidate_profile'),
    path('candidate_search/', views.candidate_search, name='candidate_search'),
]