from django.db.models import Sum

from study.models import Questions, ChoicesForQuestions, TextAnswerForQuestions


def calculate_test_field(test):
    """
    Calculate question_total_count and total_score for model Tests.
    :param: test is model Tests
    """
    questions = Questions.objects.filter(test=test)
    question_total_count = questions.count()

    total_choices_score = 0
    total_text_score = 0

    for question in questions:
        choices_score = ChoicesForQuestions.objects.filter(question=question).aggregate(total_score=Sum('score'))[
                            'total_score'] or 0
        total_choices_score += choices_score

        texts_score = TextAnswerForQuestions.objects.filter(question=question).aggregate(total_score=Sum('score'))[
                          'total_score'] or 0
        total_text_score += texts_score

    total_score = total_choices_score + total_text_score

    return question_total_count, total_score
