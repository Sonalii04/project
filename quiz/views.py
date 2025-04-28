import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import Quiz, Question, Answer
from django.utils import timezone
    
@login_required
def quiz_list(request):
    quizzes = Quiz.objects.select_related('category').prefetch_related('tags').all()
    quizzes = Quiz.objects.all()
    today = timezone.now()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes, 'today': today})


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.question_set.all())
    random.shuffle(questions)
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected and question.answer_set.filter(id=int(selected), is_correct=True).exists():
                score += 1
        UserQuizAttempt.objects.create(user=request.user, quiz=quiz, score=score)
        return render(request, 'quiz/quiz_result.html', {'score': score, 'total': len(questions), 'quiz': quiz})
    q_and_answers = []
    for q in questions:
        answers = list(q.answer_set.all())
        random.shuffle(answers)
        q_and_answers.append((q, answers))
    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'q_and_answers': q_and_answers})

@login_required
def leaderboard(request):
    attempts = UserQuizAttempt.objects.select_related('user', 'quiz').order_by('-score', 'date')[:10]
    return render(request, 'quiz/leaderboard.html', {'attempts': attempts})

from django.shortcuts import render
from .models import UserQuizAttempt
from django.contrib.auth.decorators import login_required
from collections import defaultdict

@login_required
def user_progress(request):
    attempts = UserQuizAttempt.objects.filter(user=request.user).select_related('quiz__category').order_by('date')

    # Group attempts by subject
    subject_data = defaultdict(lambda: {'labels': [], 'scores': []})
    for attempt in attempts:
        subject = attempt.quiz.category.name  # Use `quiz.subject.name` if it's called subject
        subject_data[subject]['labels'].append(attempt.date.strftime("%Y-%m-%d %H:%M"))
        subject_data[subject]['scores'].append(attempt.score)

    # Overall statistics
    all_scores = [a.score for a in attempts]
    average_score = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0

    context = {
        'subject_data': dict(subject_data),
        'attempts': attempts,
        'stats': {
            'avg_score': average_score,
            'total': len(all_scores)
        }
    }

    return render(request, 'quiz/user_progress.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerFormSet

@login_required
def add_question(request):
    """
    Display a form to create a Question and four Answers inline.
    """
    if request.method == 'POST':
        q_form = QuestionForm(request.POST)
        formset = AnswerFormSet(request.POST)
        if q_form.is_valid() and formset.is_valid():
            question = q_form.save()
            # tie the inline answers to the newly created question
            formset.instance = question
            formset.save()
            return redirect('quiz_list')
    else:
        q_form = QuestionForm()
        formset = AnswerFormSet()

    return render(request, 'quiz/add_question.html', {
        'q_form': q_form,
        'formset': formset
    })

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Quiz, UserQuizAttempt
from django.db.models import Avg, Count
import json

@login_required
def subject_list(request):
    categories = Category.objects.all()
    return render(request, 'quiz/subject_list.html', {
        'categories': categories
    })

@login_required
def quiz_list_by_subject(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    quizzes = Quiz.objects.filter(category=category) \
                  .select_related('category').prefetch_related('tags')
    return render(request, 'quiz/quiz_list.html', {
        'quizzes': quizzes,
        'current_category': category
    })
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category
from .forms import CategoryForm

@login_required
def subject_list(request):
    categories = Category.objects.all()
    return render(request, 'quiz/subject_list.html', {'categories': categories})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CategoryForm
from .models import Category

@login_required
def add_subject(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')  # You must have this URL setup
    else:
        form = CategoryForm()
    return render(request, 'quiz/add_subject.html', {'form': form})

@login_required
def subject_list(request):
    categories = Category.objects.all()
    return render(request, 'quiz/subject_list.html', {'categories': categories})

@login_required
def quiz_by_subject(request, subject_id):
    quizzes = Quiz.objects.filter(category_id=subject_id)
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')



def quiz_result(request, score, total):
    return render(request, 'quiz/quiz_result.html', {
        'score': score,
        'total': total
    })
from django.shortcuts import render

def home(request):
    return render(request, 'quiz/home.html')

from .forms import UserRegisterForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Save profile picture
            profile = user.profile
            pic = form.cleaned_data.get('profile_picture')
            if pic:
                profile.profile_picture = pic
                profile.save()

            messages.success(request, "Registration successful!")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
