from django.urls import path
from . import views

app_name = "forumapp"

urlpatterns = [
    path("", views.home, name="home"),
    path("composing-new-question/", views.compose_new_question, name="compose_new_question"),
    path("liked-questions/", views.liked_questions, name="liked_questions"),
    path("search/", views.search, name="search"),
    path("details/<int:questionID>/", views.question_details, name="question_details"),
    path("details/<int:questionID>/add-answer/", views.add_answer, name="add_answer"),
    path("details/<int:questionID>/like-question/", views.like_question, name="like_question"),
    path("like-answer/<int:answerID>", views.like_answer, name="like_answer"),
    path("show-my-questions/", views.show_my_questions, name="show_my_questions"),
    path("show-my-questions/<int:questionID>/edit-question/", views.edit_question, name="edit_question"),
    path("show-my-questions/<int:questionID>/delete-question/", views.delete_question, name="delete_question"),
]