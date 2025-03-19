from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponseForbidden

from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from users.forms import UserCreationForm, UserUpdateForm
from users.models import User
from users.utils import generate_random_password


class UsersPermissions(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(
            name='Супервайзер') or self.request.user.groups.filter(name='Руководитель КЦ')

    def handle_no_permission(self):
        return HttpResponseForbidden("Недостаточно прав")


class UsersListView(LoginRequiredMixin, UsersPermissions, ListView):
    models = User

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = context['object_list']
        return context


class UsersCreateView(LoginRequiredMixin, UsersPermissions, CreateView):
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


class UsersDeleteView(LoginRequiredMixin, UsersPermissions, DeleteView):
    model = User
    success_url = reverse_lazy('users:users')


class UsersDetailsView(LoginRequiredMixin, UsersPermissions, DetailView):
    model = User


class UsersUpdateView(LoginRequiredMixin, UsersPermissions, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_profile_update.html'
    success_url = reverse_lazy('users:users')

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
