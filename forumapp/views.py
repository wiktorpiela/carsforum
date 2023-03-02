from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

def home(request):
    wall = Question.objects.order_by("-create_date")
    return render(request, "home.html", {"wall": wall})

def question_details(request, questionID):
    question = get_object_or_404(Question, pk=questionID)

    if question.likes.filter(id=request.user.id).exists():
        question.is_liked = True
    else:
        question.is_liked = False

    answers = Answer.objects.filter(question=question.id)

    for answer in answers:
        if answer.likes.filter(id=request.user.id).exists():
            answer.is_liked = True
        else:
            answer.is_liked = False

    return render(request, "question_details.html", {"question":question, "answers":answers})

def compose_new_question(request):
    if request.method == "GET":
        return render(request, "compose_new_question.html")
    else:
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.user = request.user
            new_question.save()
            return redirect("forumapp:home")
        else:
            message = "Something went wrong, please try again!"
            return render(request, "compose_new_question.html", {"message":message})
        
def add_answer(request, questionID):
    question = get_object_or_404(Question, pk=questionID)
    return render(request, "add_answer.html", {"question":question})
