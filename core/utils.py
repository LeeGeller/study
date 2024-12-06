import re
from pprint import pprint
from typing import Dict, Any

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


def get_sorted_questions_data(test_data: QueryDict) -> list[dict]:
    questions_data = {}

    for key, value in test_data:

        question_match = re.match(r'questions\[(\d+)\]\[(\w+)\]', key)
        if question_match:
            index_question, field_question = question_match.groups()
            index_question = int(index_question)
            question = questions_data.setdefault(index_question, {"choices": []})

            if field_question == "choices":

                choice_match = re.match(r'choices\[(\d+)\]\[(\w+)\]', key)
                if choice_match:
                    index_choice, field_choice = choice_match.groups()
                    index_choice = int(index_choice)


                    while len(questions_data[index_question]["choices"]) <= index_choice:
                        questions_data[index_question]["choices"].append({})
                    questions_data[index_question]["choices"][index_choice][field_choice] = value
            else:
                # Прямое поле вопроса (например, name_of_question или answer_type)
                questions_data[index_question][field_question] = value

    # Отладочная информация
    print("Распарсенные данные вопросов:")
    pprint(questions_data)


def save_questions(questions_data: list[Dict[str, Any]], test) -> None:
    # Сохраняем вопросы и варианты ответов
    for question_data in questions_data:
        name_of_question = question_data.get("name_of_question")
        answer_type = question_data.get("answer_type")

        # Создаем вопрос
        print(f"Создаем вопрос: {name_of_question}, {answer_type}")
        question = Questions.objects.create(
            name_of_question=name_of_question,
            test=test,
            answer_type=answer_type,  # Предполагаем, что в модели Questions есть это поле
        )

        # Обрабатываем варианты ответов для типов "one_answer" и "multiple_answers"
        if answer_type in ("one_answer", "multiple_answers"):
            for choice_data in question_data["choices"]:
                name_of_choice = choice_data.get("name_of_choice")
                is_correct = choice_data.get("is_correct") == "on"
                score = choice_data.get("score")
                score = int(score) if score and score.isdigit() else 0

                print(f"Добавляем вариант ответа: {name_of_choice}, правильный: {is_correct}, баллы: {score}")
                ChoicesForQuestions.objects.create(
                    question=question,
                    name_of_choice=name_of_choice,
                    is_correct=is_correct,
                    score=score,
                )

        # Обрабатываем текстовые ответы
        elif answer_type == "text":
            text_answer = question_data.get("text_answer")
            print(f"Добавляем текстовый ответ: {text_answer}")
            TextAnswerForQuestions.objects.create(
                question=question,
                text_answer=text_answer,
            )

    return questions_data
