from django.db.models import Sum

from study.models import Questions, ChoicesForQuestions, TextAnswerForQuestions


def calculate_test_field(test):
    """
    Calculate question_total_count and total_score for model Tests.
    :param: test is model Tests
    """
    questions = test.questions.all()
    question_total_count = questions.count()

    choices_score = (
            ChoicesForQuestions.objects.filter(question__in=questions)
            .aggregate(total_score=Sum('score'))['total_score'] or 0
    )

    texts_score = (
            TextAnswerForQuestions.objects.filter(question__in=questions).aggregate(total_score=Sum('score'))[
                'total_score'] or 0
    )

    total_score = choices_score + texts_score

    return question_total_count, total_score
