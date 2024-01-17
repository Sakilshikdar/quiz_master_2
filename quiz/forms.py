from .models import Rating
from .models import Quiz, Question
from django import forms
from .models import Quiz, Question, Choice


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category', 'has_time_limit']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'point_value']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']


# forms.py


class QuizForm(forms.Form):
    def __init__(self, *args, quiz=None, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.quiz = quiz
        print(self.quiz)
        for question in quiz.questions.all():
            choices = [(choice.id, choice.text)
                       for choice in question.choices.all()]

            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=choices,
                widget=forms.RadioSelect,
                required=True
            )

    def calculate_score(self):
        score = 0
        for question in self.quiz.questions.all():
            selected_choice_id = self.cleaned_data.get(
                f'question_{question.id}')
            correct_choice = question.choices.filter(is_correct=True).first()
            if selected_choice_id == str(correct_choice.id):
                score += 1
        return score


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.RadioSelect
        }
