from django.db import models
from django.db.models.expressions import OrderBy
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ("id",)

    def __str__(self):
        return self.title


class UpdatedQuestion(models.Model):
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Question(UpdatedQuestion):
    SCALE = (
        (0, _('Fundamental')),
        (1, _('Beginner')),
        (2, _('Intermedia')),
        (3, _('Advanced')),
        (4, _('Expert')),
    )

    TYPE = (
        (0, _("Multiple Choice")),
    )

    quiz = models.ForeignKey(Quiz, related_name="question", on_delete=models.DO_NOTHING)
    technique = models.IntegerField(choices=TYPE, default=0)
    title = models.CharField(max_length=255)
    difficulty = models.IntegerField(choices=SCALE, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ("id",)


class Answer(UpdatedQuestion):
    question = models.ForeignKey(Question, related_name="answer", on_delete=models.DO_NOTHING)
    answer_text = models.CharField(max_length=255)
    is_right = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ("id",)
