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

    return questions_data


def save_questions(questions_data: dict, test) -> None:
    print(questions_data)
    for index_questions, data_questions in questions_data.items():
        print(data_questions)

        name_of_question = data_questions.get("name_of_question")
        answer_type = data_questions.get("answer_type")

        question = Questions.objects.create(
            name_of_question=name_of_question,
            test=test,
        )

        if answer_type in ["one_answer", "multiple_answers"]:
            for data in data_questions["choices"]:
                name_of_choice = data.get("name_of_choice")
                score = 0 if data.get("score", 0) == "" else int(data.get("score"))
                right_answer = data.get("is_correct") == "on"

                print(name_of_choice, score, right_answer)

                ChoicesForQuestions.objects.create(
                    name_of_choice=name_of_choice,
                    question=question,
                    right_answer=right_answer,
                    score=score,
                )
        # elif answer_type == "text":
        #     text_answer = data_questions["choices"].get("text_answer")
        #     TextAnswerForQuestions.objects.create(
        #         question=question,
        #         text_answer=text_answer,
        #     )
