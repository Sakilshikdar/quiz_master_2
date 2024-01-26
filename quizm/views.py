from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Quiz, Category
from django.db.models import Q
from quizm.models import QuizSubmission
from django.contrib import messages
from author.models import Profile


@login_required(login_url='user_login')
def all_quiz_view(request):

    quizzes = Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()
    for quiz in quizzes:
        print(quiz.image)
    context = {"user_profile": 'sakil',
               "quizzes": quizzes, "categories": categories}
    return render(request, 'all-quiz.html', context)


@login_required(login_url='user_login')
def search_view(request, category):

    user_object = User.objects.get(username=request.user)

    if request.GET.get('q') != None:
        q = request.GET.get('q')
        query = Q(title__icontains=q) | Q(description__icontains=q)
        quizzes = Quiz.objects.filter(query).order_by('-created_at')

    # search by category
    elif category != " ":
        quizzes = Quiz.objects.filter(
            category__name=category).order_by('-created_at')

    else:
        quizzes = Quiz.objects.order_by('-created_at')

    categories = Category.objects.all()

    context = {"user_profile": 'sakil',
               "quizzes": quizzes, "categories": categories}
    return render(request, 'all-quiz.html', context)


@login_required(login_url='user_login')
def quiz_view(request, quiz_id):
    user_object = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    total_questions = quiz.question_set.all().count()

    if request.method == "POST":
        # Get the score
        score = int(request.POST.get('score', 0))

        # Get the previous submission for the same quiz
        previous_submission = QuizSubmission.objects.filter(
            user=user_object, quiz=quiz).first()

        # Check if the user has already submitted the quiz and if the new score is greater
        if previous_submission and score > previous_submission.score:
            # Update the score in the existing submission
            previous_submission.score = score
            previous_submission.save()

            messages.success(
                request, f"Your score  {score} out of {total_questions}")
        elif not previous_submission:
            # Save the new quiz submission if it's the first submission
            submission = QuizSubmission(
                user=user_object, quiz=quiz, score=score)
            submission.save()
            messages.success(
                request, f"Quiz submitted successfully. You got {score} out of {total_questions}")
        else:
            messages.success(
                request, f"You already submitted a higher score of {previous_submission.score} out of {total_questions}")

        return redirect('quiz', quiz_id)

    context = {"user_profile": 'sakil', "quiz": quiz}
    return render(request, 'quiz.html', context)
