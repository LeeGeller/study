from django.contrib import admin

from study.models import Tests, Questions, ChoicesForQuestions, TextAnswerForQuestions, UserTestAssignment


@admin.register(Tests)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_test', 'is_active', 'questions_count', 'total_score',)
    list_filter = ('is_active',)
    search_fields = ('name_of_test',)


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_question', 'test',)
    list_filter = ('test',)
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
    list_display = ('id', 'user', 'test', 'attempts', 'attempt_at', 'status',)
    list_filter = ('user',)
    search_fields = ('user', 'users_test',)
