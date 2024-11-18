from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from study.models import Questions, ChoicesForQuestions, TextAnswerForQuestions, Tests


@receiver([post_save, post_delete], sender=Questions)
def update_questions_count(sender, instance, **kwargs):
    test = instance.test
    test.questions_count = test.questions.count()
    test.save()


@receiver([post_save, post_delete], sender=Tests)
def update_tests_score(sender, instance, **kwargs):
    if getattr(instance, '_is_updating', False):
        return

    instance._is_updating = True
    try:
        questions = Questions.objects.filter(test=instance)

        total_choices_score = 0
        total_text_score = 0

        for question in questions:
            choices_score = ChoicesForQuestions.objects.filter(question=question).aggregate(total_score=Sum('score'))[
                                'total_score'] or 0
            total_choices_score += choices_score

            texts_score = TextAnswerForQuestions.objects.filter(question=question).aggregate(total_score=Sum('score'))[
                              'total_score'] or 0
            total_text_score += texts_score

        # Обновляем поле total_score теста
        instance.total_score = total_choices_score + total_text_score
        instance.save()

    finally:
        instance._is_updating = False
