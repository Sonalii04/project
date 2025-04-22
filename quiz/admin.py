# from django.contrib import admin
# from .models import Subject, Question, UserScore

# # Register your models here.
from django.contrib import admin
from .models import Quiz, Question, Answer, UserQuizAttempt

admin.site.register(UserQuizAttempt)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Quiz)
