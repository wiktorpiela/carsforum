from django.urls import path
from . import views

app_name = "forumapp"

urlpatterns = [
    path("", views.home, name="home"),
    path("composing-new-question/", views.compose_new_question, name="compose_new_question"),
    path("details/<int:questionID>/", views.question_details, name="question_details"),
    path("details/<int:questionID>/add-answer/", views.add_answer, name="add_answer"),
    path("show-my-questions/", views.show_my_questions, name="show_my_questions"),
    path("show-my-questions/<int:questionID>/edit-question/", views.edit_question, name="edit_question"),
]