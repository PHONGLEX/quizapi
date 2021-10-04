from rest_framework import serializers

from .models import *


class QuestionSerializer(serializers.ModelSerializer):
    quiz_id = serializers.IntegerField()
    class Meta:
        model = Question
        fields = ("quiz_id", "technique", "title", "difficulty", "is_active",)



class QuizSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    class Meta:
        model = Quiz
        fields = ("category_id", "title")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    class Meta:
        model = Answer
        fields = ("question_id", "answer_text", "is_right")
