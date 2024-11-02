from sndhdr import tests

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


class Tests(models.Model):
    name_of_test = models.CharField(
        max_length=300, verbose_name='Название теста', unique=True,
        help_text='Название теста'
    )
    question_count = models.PositiveIntegerField(default=0, verbose_name="Общее количество вопросов")

    def __str__(self):
        return self.name_of_test

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Questions(models.Model):
    name_of_question = models.TextField(verbose_name='Вопрос', help_text='Введите вопро ')
    test = models.ForeignKey(Tests, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.name_of_question


class ChoicesForQuestions(models.Model):
    name_of_choice = models.TextField(verbose_name='Вариант ответа', help_text='Введите вариант ответа')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answer_choices')
    right_answer = models.BooleanField(verbose_name='Правильный ответ', default=False)

    def __str__(self):
        return self.name_of_choice

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'


class TextAnswerForQuestions(models.Model):
    answer = models.TextField(verbose_name='Ответ', help_text='Ваш ответ')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='text_answers', null=True)
    right_answer = models.BooleanField(verbose_name='Правильный ответ', default=False)


class UserTestAssignment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='test_assignments',
                             verbose_name='Оператор')
    test = models.ForeignKey(Tests, on_delete=models.CASCADE, related_name='user_assignments')


@receiver([post_save, post_delete], sender=Questions)
def update_question_count(sender, instance, **kwargs):
    test = instance.test
    tests.question_count = test.questions.count()
    test.save()
