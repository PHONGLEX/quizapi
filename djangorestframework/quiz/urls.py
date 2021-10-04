from django.urls import path

from . import views


urlpatterns = [
    path('category/', views.CategoryCreateView.as_view(), name='category'),
    path('quiz/', views.QuizCreateView.as_view(), name='quiz'),
    path('question/', views.QuestionListCreateView.as_view(), name='question'),
    path('answer/', views.AnswerListCreateView.as_view(), name='answer-list'),
    path('answer/<pk>/detail', views.AnswerDetailView.as_view(), name='answer-detail'),
]