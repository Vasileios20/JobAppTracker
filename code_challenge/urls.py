from django.urls import path
from . import views

urlpatterns = [
   path('', views.code_challenge_view, name='code_challenge'),
   path('code/submit/', views.submit_solution, name='submit_solution'),
   path('code/challenges/<slug:slug>/',
        views.challenge_detail_view, name='challenge_detail'),
]
