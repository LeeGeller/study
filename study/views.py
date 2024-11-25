import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from core.utils import get_questions_data
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


class TestsCreateView(CreateView):
    model = Tests
    fields = ['name_of_test', ]
    success_url = reverse_lazy('tests_list')

    def form_valid(self, form):
        test = form.save()
        print(type(test))
        test_data = self.request.POST.items()
        test_info = get_questions_data(test_data)

    # return super().form_valid(form)
