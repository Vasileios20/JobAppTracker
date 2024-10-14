from django.urls import path
from .views import GenerateInterviewQuestionsView, EvaluateInterviewAnswersView

urlpatterns = [
    path('', GenerateInterviewQuestionsView.as_view(),
         name='practice_interview'),
    path('evaluate/', EvaluateInterviewAnswersView.as_view(),
         name='evaluate_answers'),
]
