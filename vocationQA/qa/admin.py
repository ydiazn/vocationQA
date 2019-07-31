from django.contrib import admin
from . import models

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'body', 'user', 'created')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'body', 'user', 'created')


admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)