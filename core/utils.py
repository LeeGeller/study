import re

from django.http import QueryDict

from study.models import ChoicesForQuestions, Questions


def get_sorted_questions_data(test_data: QueryDict) -> dict[int:dict[str:str | int], str:str]:
    questions_data = {}
    test_data = dict(test_data)

    for key, value in test_data.items():

        question_match = re.match(r'questions\[(\d+)\]\[(\w+)\]', key)
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
    print(test_data)

    return questions_data


def save_questions(questions_data: dict, test) -> None:
    for index_questions, data_questions in questions_data.items():

        answer_type = data_questions.get("answer_type")

        question = Questions.objects.create(
            name_of_question=data_questions.get("name_of_question"),
            test=test,
        )
        print(questions_data)

        if answer_type in ["one_answer", "multiple_answers"]:
            for data in data_questions["choices"]:
                name_of_choice = data.get("name_of_choice")
                score = 0 if data.get("score", 0) == "" else int(data.get("score"))
                right_answer = data.get("is_correct") == "on"

                ChoicesForQuestions.objects.create(
                    name_of_choice=name_of_choice,
                    question=question,
                    right_answer=right_answer,
                    score=score,
                )
    print(test)

    test.update_tests_statistics()
    print('Did update tests statistics')
    # elif answer_type == "text":
    #     text_answer = data_questions["choices"].get("text_answer")
    #     TextAnswerForQuestions.objects.create(
    #         question=question,
    #         text_answer=text_answer,
    #     )
