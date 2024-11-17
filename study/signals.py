from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from study.models import Questions, Tests, ChoicesForQuestions


@receiver([post_save, post_delete], sender=Questions)
def update_questions_count(self, instance, **kwargs):
    test = instance.test
    test.questions_count = test.question_count.count()
    test.save()

receiver([post_save, post_delete], sender=Tests)
def update_tests_score(self, instance, **kwargs):
    question = instance
    choices_score = ChoicesForQuestions.objects.filter()