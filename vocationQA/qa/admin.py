from django.contrib import admin
from .models import Question

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'body', 'user', 'created')


admin.site.register(Question, QuestionAdmin)