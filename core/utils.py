import re

from django.http import QueryDict

from study.models import ChoicesForQuestions, Questions
import logging

logger = logging.getLogger(__name__)


def get_sorted_questions_data(test_data: QueryDict) -> dict:
    questions_data = {}
    logger.info(test_data)
    test_data = dict(test_data)
    print(test_data)

    for key, value in test_data.items():

        question_match = re.match(r'questions\[(\d+)\]\[(\w+)\]', key)
        logger.info(f"Processing key: {key}, value: {value}")
        if question_match:
            index_question, field_question = question_match.groups()
            index_question = int(index_question)

            if index_question not in questions_data:
                questions_data[index_question] = {"choices": []}

            if field_question == "choices":
                choice_match = re.match(r'questions\[\d+\]\[choices\]\[(\d+)\]\[(\w+)\]', key)
                if choice_match:
                    index_choice, field_choice = choice_match.groups()
                    index_choice = int(index_choice)

                    while len(questions_data[index_question]["choices"]) <= index_choice:
                        questions_data[index_question]["choices"].append({})

                    questions_data[index_question]["choices"][index_choice][field_choice] = value
            else:
                questions_data[index_question][field_question] = value
    logger.info(f"Processed questions data: {questions_data}")

    return questions_data


def save_questions(questions_data: dict, test) -> None:
    for index_questions, data_questions in questions_data.items():
        logger.info(f"Saving question: {data_questions}")

        answer_type = data_questions.get("answer_type")

        question = Questions.objects.create(
            name_of_question=data_questions.get("name_of_question"),
            test=test,
        )
        question.save()

        if answer_type in ["one_answer", "multiple_answers"]:
            for data in data_questions["choices"]:
                name_of_choice = data.get("name_of_choice")
                score = int(data.get("score", 0))
                right_answer = data.get("is_correct") == "on"

                choices = ChoicesForQuestions.objects.create(
                    name_of_choice=name_of_choice,
                    question=question,
                    right_answer=right_answer,
                    score=score,
                )
                choices.save()
    print(test)

    test.update_tests_statistics()
    print('Did update tests statistics')
    # elif answer_type == "text":
    #     text_answer = data_questions["choices"].get("text_answer")
    #     TextAnswerForQuestions.objects.create(
    #         question=question,
    #         text_answer=text_answer,
    #     )
