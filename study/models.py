from django.db import models

class Tests(models.Model):
    name_of_test = models.CharField(
        max_length=300, verbose_name='Название теста', unique=True,
        help_text='Название теста'
    )

    def __str__(self):
        return self.name_of_test

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

class Questions(models.Model):
    name_of_question = models.TextField(verbose_name='Вопрос', unique=True, help_text='Введите вопро ')
    test = models.ForeignKey(Tests, on_delete=models.SET_NULL, related_name='test')

    def __str__(self):
        return self.name_of_question

class ChoicesForQuestions(models.Model):
    name_of_choice = models.TextField(verbose_name='Вариант ответа', unique=True, help_text='Введите вариант ответа')
    question = models.ForeignKey(Questions, on_delete=models.SET_NULL, related_name='answer_choice')
    right_answer = models.BooleanField(verbose_name='Правильный ответ', default=False)

    def __str__(self):
        return self.name_of_choice

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

class TextAnswerForQuestions(models.Model):
    answer = models.TextField(verbose_name='Ответ', help_text='Ваш ответ')
    question = models.ForeignKey(Questions, on_delete=models.SET_NULL, related_name='answer_text')
    right_answer = models.BooleanField(verbose_name='Правильный ответ', default=False)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'
