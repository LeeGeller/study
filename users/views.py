from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import ListView, CreateView

from users.forms import UserCreationForm
from users.models import User
from users.utils import generate_random_password


class UsersListView(LoginRequiredMixin, ListView):
    models = User

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = context['object_list']
        return context


class UsersCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('users:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')

        if not password:
            password = generate_random_password()

        user.set_password(password)

        user.save()

        return super().form_valid(form)


@require_GET
def generate_password_view(request):
    password = generate_random_password()
    return JsonResponse({'password': password})
