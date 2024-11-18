from django.contrib import admin
from django.db.models import Count

from study.models import Tests, Questions, ChoicesForQuestions, TextAnswerForQuestions, UserTestAssignment


@admin.register(Tests)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_test', 'is_active', 'questions_count', 'total_score',)
    list_filter = ('is_active',)
    search_fields = ('name_of_test',)

    def get_questions_count(self, obj):
        return obj.questions_count

    get_questions_count.short_description = 'Количество вопросов'

    def get_tests_score(self, obj):
        return obj.questions_set.aggregate(count=Count('choicesforquestions'))['count']

    get_tests_score.short_description = 'Количество вариантов ответов'


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_question', 'test', 'question_score',)
    list_filter = ('question_score',)
    search_fields = ('name_of_question',)


@admin.register(ChoicesForQuestions)
class ChoicesForQuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_choice', 'question', 'right_answer', 'score',)
    list_filter = ('score',)
    search_fields = ('name_of_choice',)


@admin.register(TextAnswerForQuestions)
class TextAnswerForQuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'question', 'right_answer', 'score',)
    list_filter = ('score',)
    search_fields = ('answer',)


@admin.register(UserTestAssignment)
class UserTestAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'users_test', 'attempts', 'attempt_at', 'status',)
    list_filter = ('user',)
    search_fields = ('user', 'users_test',)
