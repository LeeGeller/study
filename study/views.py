from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView

from core.utils import get_sorted_questions_data, save_questions
from study.models import Tests


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = context['object_list']
        return context


class TestsCreateView(CreateView):
    model = Tests
    fields = ['name_of_test', 'is_active', 'questions_count', 'total_score']
    success_url = reverse_lazy('tests_list')

    def form_valid(self, form):
        test = form.save()
        try:
            test_data = self.request.POST
            sorted_questions_data = get_sorted_questions_data(test_data)
            save_questions(sorted_questions_data, test)
        except Exception as e:
            print(f"Error during test creation: {e}")
            messages.error(self.request, "Ошибка при сохранении теста. Проверьте данные.")
            return self.form_invalid(form)
        return redirect(self.success_url)


class TestsDetailView(DetailView):
    model = Tests
    fields = ['pk', 'name_of_test', 'is_active', 'questions_count', 'total_score']


class TestsDeleteView(DeleteView):
    model = Tests
    template_name = 'study/tests_confirm_delete.html'
    success_url = reverse_lazy('tests_list')
