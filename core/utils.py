import re

from django.db.models import Sum

from study.models import ChoicesForQuestions, TextAnswerForQuestions


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


def get_questions_data(test_data: dict) -> list[dict]:
    questions_data = []
    print(test_data)

    for questions, val in test_data:
        print(questions, val)
        if questions.startswith('questions['):
            question_match = re.match(r'questions\[(\d+)\]\[(\w+)\]', questions)
            print(question_match)
            if question_match:
                index_question, field_question = question_match.groups()
                index_question = int(index_question)
                while len(questions_data) <= index_question:
                    questions_data.append({'choices': []})
                    print(1, 'questions_data')
                if field_question == 'choices':
                    choice_match = re.match(r'choices\[(\d+)\]\[(\w+)\]', questions)
                    if choice_match:
                        index_choices, field_choices = choice_match.groups()
                        index_choices = int(index_choices)
                        while len(questions_data[index_question]['choices']) <= index_choices:
                            questions_data[index_question]['choices'].append({})
                            print(2, 'questions_data')
                        questions_data[index_question]['choices'][index_choices][field_choices] = val
                        print(3, 'questions_data')
                else:
                    questions_data[index_question][field_question] = val

    #     if question.startswith('questions['):
    #         questions_info = re.match(r'questions\[(\d+)\]\[(\w+)\]', question)
    #         if questions_info:
    #             index_question, field_question = questions_info.groups()
    #             if len(questions_data) <= int(index_question):
    #                 questions_data.append({})
    #             questions_data[int(index_question)][field_question] = val
    #
    # print(questions_data)
    #
    # for question_data in questions_data:
    #     name_of_question = question_data.get('name_of_question')
    #     print(name_of_question)
    #     question = Questions.objects.create(name_of_question=name_of_question, test=self.object)
    #     print(question)
    #
    #     choices_data = question_data.get('choices', [])
    #     print(choices_data)
    #     if choices_data:
    #         for choice_data in choices_data:
    #             name_of_choice = choice_data.get('name_of_choice')
    #             print(name_of_choice)
    #             right_choice = choice_data.get('is_correct')
    #             print(right_choice)
    #             score = choice_data.get('score')
    #             print(score)
    #
    #             choice = ChoicesForQuestions.objects.create(
    #                 question=question,
    #                 name_of_choice=choice_data.get('name_of_choice'),
    #                 is_correct=right_choice,
    #                 score=score,
    #             )
    #
    #             print(choice)

# for question_id in questions_data:
#     try:
#         question = Questions.objects.get(id=question_id)
#         question.test = self.object
#         question.save()
#     except Questions.DoesNotExist:
#         continue
#
#
# question_total_count, total_score = calculate_test_field(self.object)
# self.object.total_score = total_score
# self.object.questions_count = question_total_count
# self.object.save()
