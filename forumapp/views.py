from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

def home(request):
    wall = Question.objects.order_by("-create_date")
    for question in wall:
        if question.user == request.user:
            question.is_your_question = True
        else:
            question.is_your_question = False
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

@login_required
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

@login_required    
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

@login_required
def show_my_questions(request):
    my_questions = Question.objects.filter(user=request.user)
    return render(request, "show_my_questions.html", {"my_questions":my_questions})

@login_required
def edit_question(request, questionID):
    my_question = get_object_or_404(Question, pk=questionID, user=request.user)
    form = QuestionForm(instance=my_question)
    if request.method == "GET":
        return render(request, "edit_question.html", {"my_question":my_question, "form":form})
    else:
        quest = QuestionForm(request.POST, request.FILES, instance=my_question)
        if quest.is_valid():
            quest.save()
            return redirect("forumapp:show_my_questions")
        else:
            message = "Somethign went wrong, please try again."
            return render(request, "edit_question.html", {"my_question":my_question, "form":form})
        
@login_required
def delete_question(request, questionID):
    my_question = get_object_or_404(Question, pk=questionID, user=request.user)
    my_question.delete()
    return redirect("forumapp:show_my_questions")

@login_required
def like_question(request, questionID):
    question = get_object_or_404(Question, pk=questionID)
    isLiked = question.likes.filter(id = request.user.id)
    if isLiked:
        question.likes.remove(request.user)
    else:
        question.likes.add(request.user)
    return redirect("forumapp:question_details", questionID=questionID)

@login_required
def like_answer(request, answerID):
    answer = get_object_or_404(Answer, pk=answerID)
    isLiked = answer.likes.filter(id = request.user.id)
    if isLiked:
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return redirect("forumapp:question_details", questionID=answer.question.id)

@login_required
def liked_questions(request):
    likedQuestions = User.objects.prefetch_related('likes').get(pk=request.user.id).likes.all()
    for question in likedQuestions:
        if question.user == request.user:
            question.is_your_question = True
        else:
            question.is_your_question = False
    return render(request, "liked_questions.html", {"likedQuestions":likedQuestions})

def search(request):
    keywords = request.POST.get("search").split(" ")
    for word in keywords:
        queryset = Question.objects.filter(
            Q(title__icontains = word) | Q(desc__icontains = word)
        )
        try:
            questions = questions | queryset
        except UnboundLocalError:
            questions = queryset

    questions = questions.order_by("create_date")

    return render(request, "filtered_questions.html", {"questions":questions})
    





