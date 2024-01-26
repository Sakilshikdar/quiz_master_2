from django.urls import path
from .views import create_quiz, add_question, add_choice, quiz_list, quiz_detail, user_dashboard, quiz_ratting

urlpatterns = [
    path('create/', create_quiz, name='create_quiz'),
    path('<int:quiz_id>/add-question/', add_question, name='add_question'),
    path('<int:question_id>/add-choice/', add_choice, name='add_choice'),
    path('quizzes/', quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path('dashboard/<str:username>', user_dashboard, name='user_dashboard'),
    path('quiz/<int:quiz_id>/rate/', quiz_ratting, name='rate_quiz'),

]
