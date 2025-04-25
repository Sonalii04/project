# from django.contrib import admin
# from .models import Subject, Question, UserScore

# # Register your models here.
from django.contrib import admin
from .models import Quiz, Question, Answer, UserQuizAttempt

admin.site.register(UserQuizAttempt)
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Question, QuestionAdmin)

admin.site.register(Answer)
admin.site.register(Quiz)
