from django.contrib import admin
from .models import Question, Answer

class CreateDate(admin.ModelAdmin):
    readonly_fields = ("create_date",)

admin.site.register(Question, CreateDate)
admin.site.register(Answer, CreateDate)
