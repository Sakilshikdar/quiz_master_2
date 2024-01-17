from django.contrib.auth.models import User
from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    has_time_limit = models.BooleanField(default=False)
    time_limit_minutes = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0, blank=True, null=True)

    def calculate_average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            total_rating = sum([rating.value for rating in ratings])
            self.average_rating = total_rating / len(ratings)
        else:
            self.average_rating = 0.0
        self.save()


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    point_value = models.IntegerField(default=1)


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name='choices', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    @property
    def quiz_title(self):
        print(self)
        return self.question.quiz.title


class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    completed_quizzes = models.ManyToManyField(
        'Quiz', related_name='completed_by', blank=True)

    def get_score_for_quiz(self, quiz):
        score = 0
        for question in quiz.questions.all():
            score += question.point_value
        return score


class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 8)])
