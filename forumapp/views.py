from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.mail import EmailMessage
from django.conf import settings

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
    if request.method == "GET":
        return render(request, "add_answer.html", {"question":question})
    else:
        form = AnswerForm(request.POST, request.FILES)
        author_email = request.user.email
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.user = request.user
            new_answer.question = question
            new_answer.save()

            if question.user != request.user:
                email = EmailMessage(
                    f"Your question '{question.title}' has been asnwered by {request.user.username}",
                    f"""Congratulations, <br>
                    {request.user.username} has just added the answer to your question!
                    Content of the response:
                    {new_answer.desc} <br>
                    Best regards, Cars Forum""",
                    settings.DEFAULT_FROM_EMAIL,
                    [author_email])
                email.content_subtype = "html"
                email.send()
                return redirect("forumapp:question_details", questionID=question.id)
            else:
                return redirect("forumapp:question_details", questionID=question.id)
    
        else:
            message = "Something went wrong, please try again!"
            return render(request, "add_answer.html", {"question":question, "message":message})
                


