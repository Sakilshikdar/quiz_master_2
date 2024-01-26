from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from author.models import Profile
from quizm.models import UserRank
from django.contrib.auth.models import User
from quizm.models import QuizSubmission
from quizm.models import Quiz, Category


def home(request, category_slug=None):

    quizzes = Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()
    context = {"user_profile": 'sakil',
               "quizzes": quizzes, "categories": categories}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html',)


def contact(request):
    return render(request, 'contact.html',)


@login_required(login_url="user_login")
def leaderboard_view(request):

    submissions = QuizSubmission.objects.all()
    user_object = User.objects.get(username=request.user)
    # user_profile = Profile.objects.get(user=user_object)

    leaderboard_users = UserRank.objects.order_by('rank')
    for rank in leaderboard_users:
        print(rank.user.username)
    print(leaderboard_users)

    context = {"leaderboard_users": leaderboard_users,
               "user_profile": 'sakil', "submissions": submissions}
    return render(request, "leaderboard.html", context)
