from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ("create_date", "likes", "user",)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("desc", "image",)