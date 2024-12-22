from django.db import models


class Tests(models.Model):
    name_of_test = models.CharField(
        max_length=300, verbose_name='Название теста', unique=True,
        help_text='Название теста'
    )
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    questions_count = models.PositiveIntegerField(default=0, verbose_name='Количество вопросов')
    total_score = models.PositiveIntegerField(default=0, verbose_name='Общее количество очков')

    def __str__(self):
        return self.name_of_test

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Questions(models.Model):
    name_of_question = models.TextField(verbose_name='Вопрос', unique=False, help_text='Введите вопрос')
    test = models.ForeignKey(Tests, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.name_of_question


class ChoicesForQuestions(models.Model):
    name_of_choice = models.TextField(verbose_name='Вариант ответа', unique=False, help_text='Введите вариант ответа')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='choices')
    right_answer = models.BooleanField(verbose_name='Правильный ответ', default=False)
    score = models.PositiveIntegerField(verbose_name='Балл', default=0)

    def __str__(self):
        return self.name_of_choice

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'


class TextAnswerForQuestions(models.Model):
    answer = models.TextField(verbose_name='Ответ', help_text='Ваш ответ')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='text_answers')
    right_answer = models.BooleanField(verbose_name='Правильный ответ', default=False)
    score = models.PositiveIntegerField(verbose_name='Балл', default=0)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'


class UserTestAssignment(models.Model):
    CHOICES_OF_STATUS = (
        ('in_progress', 'В процессе'),
        ('passed', 'Пройден'),
        ('failed', 'Не пройден'),
    )

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='user_assignments',
        null=True, blank=True, verbose_name='Пользователь'
    )
    users_test = models.ForeignKey('study.Tests', on_delete=models.CASCADE, related_name='assigned_tests',
                                   verbose_name='Тест')
    attempts = models.PositiveIntegerField(verbose_name='Количество попыток', default=0)
    attempt_at = models.DateTimeField(verbose_name='Попытка', auto_now_add=True)
    status = models.CharField(max_length=20,
                              choices=CHOICES_OF_STATUS,
                              default='in_progress', verbose_name='Статус'
                              )
