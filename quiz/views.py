from .forms import QuizForm
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from .models import Quiz, Question, Choice, UserProgress, QuizScore
from django.db import models
from .forms import QuizForm, QuestionForm, ChoiceForm
from .models import Quiz, UserProgress
from django.contrib.auth.decorators import login_required
from .forms import RatingForm
from .models import Rating
from django.contrib.auth.models import User

from django.contrib import messages

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()

    return render(request, 'create_quiz.html', {'quiz_form': quiz_form})


def add_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            return redirect('add_choice', question_id=question.id)
    else:
        question_form = QuestionForm()

    return render(request, 'add_question.html', {'question_form': question_form, 'quiz': quiz})


def add_choice(request, question_id):
    question = Question.objects.get(id=question_id)

    if request.method == 'POST':
        choice_form = ChoiceForm(request.POST)
        if choice_form.is_valid():
            choice = choice_form.save(commit=False)
            choice.question = question
            choice.save()

            return redirect('add_choice', question_id=question.id)
    else:
        choice_form = ChoiceForm()

    return render(request, 'add_choice.html', {'choice_form': choice_form, 'question': question})


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})


score_array = []


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    length = len(quiz.questions.all())
    user_progress, created = UserProgress.objects.get_or_create(
        user=request.user)

    if request.method == 'POST':
        form = QuizForm(request.POST, quiz=quiz)
        if form.is_valid():
            score = form.calculate_score()
            user_progress.completed_quizzes.add(quiz)
            score_array.append(score)
            email_subject = "Your Quiz Result"
            email_body = render_to_string(
                'quiz_email.html', {'score': score})
            email = EmailMultiAlternatives(
                email_subject, '', to=[request.user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            messages.success(request, "Check your mail")
            return render(request, 'quiz_result.html', {'score': score, 'length': length, })
    else:
        form = QuizForm(quiz=quiz)

    return render(request, 'quiz_detail.html', {'quiz': quiz, 'form': form})


@login_required
def user_dashboard(request):
    user_progress, created = UserProgress.objects.get_or_create(
        user=request.user)
    completed_quizzes = user_progress.completed_quizzes.all()
    quiz_com = 0
    quiz_scores = {quiz.id: user_progress.get_score_for_quiz(
        quiz) for quiz in completed_quizzes}
    if score_array:
        max_score = max(score_array)
    else:
        max_score = 0
    if len(quiz_scores) > 0:
        items_list = list(quiz_scores.items())
        last = items_list[-1]
        key = last[0]
        quiz_com = key
    return render(request, 'user_dashboard.html', {'completed_quizzes': completed_quizzes, 'quiz_scores': quiz_com | 0, 'max_score': max_score})


@login_required
def quiz_ratting(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            Rating.objects.create(user=request.user, quiz=quiz, rating=rating)
            ratings = quiz.ratings.all()
            total_ratings = ratings.count()
            average_rating = sum(rating.rating for rating in ratings) / \
                total_ratings if total_ratings > 0 else 0
            quiz.average_rating = round(average_rating, 2)
            quiz.total_ratings = total_ratings
            quiz.save()

    return render(request, 'rate_quiz.html', {'quiz': quiz, 'form': RatingForm()})


def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-average_rating')
    return render(request, 'quiz_list.html', {'quizzes': quizzes})
