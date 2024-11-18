from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from study.models import Tests, Questions


class HomeListView(LoginRequiredMixin, ListView):
    model = Tests


class TestsListView(LoginRequiredMixin, ListView):
    model = Tests
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Supervisor').exists():
            return Tests.objects.all()
        else:
            return Tests.objects.filter(is_active=True)


class TestsCreateView(CreateView):
    model = Tests
    fields = ['name_of_test', ]
    success_url = reverse_lazy('tests_list')

    def form_valid(self, form):
        self.object = form.save()

        questions_data = self.request.POST.getlist('questions')

        for question_id in questions_data:
            try:
                question = Questions.objects.get(id=question_id)
                question.test = self.object
                question.save()
            except Questions.DoesNotExist:
                continue
        return super().form_valid(form)
