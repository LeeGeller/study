from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

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
    fields = ['name_of_test', 'is_active']
    success_url = reverse_lazy('tests_list')

    def form_valid(self, form):
        test = form