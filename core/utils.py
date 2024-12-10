import re
from typing import Any

from django.db.models import Sum
from django.http import QueryDict

from study.models import ChoicesForQuestions, TextAnswerForQuestions, Questions


def calculate_test_field(test) -> tuple[int, int]:
    """
    Calculate question_total_count and total_score for model Tests.
    :param: test is model Tests
    """
    if test:
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


def get_sorted_questions_data(test_data: QueryDict) -> list[dict[str, Any]]:
    questions_data = {}

    for key, value in test_data:
        print(test_data)
        print(0, key, value)

        question_match = re.match(r'questions\[(\d+)\]\[(\w+)\]', key)
        if question_match:
            index_question, field_question = question_match.groups()
            index_question = int(index_question)
            print('i', index_question)
            print('fi', field_question)
            while len(index_question) <= index_question:

                if field_question == "choices":

                    choice_match = re.match(r'choices\[(\d+)\]\[(\w+)\]', key)
                    if choice_match:
                        index_choice, field_choice = map(int, choice_match.groups())
                        print(2, questions_data)
                        choice = questions_data["choices"].setdefault(index_choice, {})
                        print(3, questions_data)
                        choice[field_choice] = value
                else:
                    questions_data[field_question] = value

    return list(questions_data.values())


def save_questions(questions_data: dict[int, dict[str, Any]], test) -> None:
    print(4, questions_data)
    for question_data in questions_data:
        print(5, question_data)
        name_of_question = question_data.get("name_of_question")
        answer_type = question_data.get("answer_type")

        print(6, {name_of_question}, {answer_type})
        question = Questions.objects.create(
            name_of_question=name_of_question,
            test=test,
            answer_type=answer_type,
        )

        print(7, questions_data)

        if answer_type in ("one_answer", "multiple_answers"):
            for choice_data in question_data["choices"]:
                name_of_choice = choice_data.get("name_of_choice")
                is_correct = choice_data.get("is_correct") == "on"
                score = choice_data.get("score")
                score = int(score) if score and score.isdigit() else 0

                print(8, {name_of_choice}, {is_correct}, {score})
                ChoicesForQuestions.objects.create(
                    question=question,
                    name_of_choice=name_of_choice,
                    is_correct=is_correct,
                    score=score,
                )

        elif answer_type == "text":
            text_answer = question_data.get("text_answer")
            print(f"Добавляем текстовый ответ: {text_answer}")
            TextAnswerForQuestions.objects.create(
                question=question,
                text_answer=text_answer,
            )
