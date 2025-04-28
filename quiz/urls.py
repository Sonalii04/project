from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import login_view, logout_view, register_view, home
urlpatterns = [
    path('', views.home, name='home'),
    path('quiz_list/', views.quiz_list, name='quiz_list'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('quiz/subject/<int:subject_id>/', views.quiz_by_subject, name='quiz_by_subject'),
    path('subjects/<int:category_id>/quizzes/', views.quiz_list_by_subject, name='quiz_list_by_subject'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('progress/', views.user_progress, name='user_progress'),
    path('add-question/', views.add_question, name='add_question'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



