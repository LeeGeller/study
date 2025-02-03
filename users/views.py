from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from users.models import User


class UsersListView(LoginRequiredMixin, ListView):
    models = User

    def get_queryset(self):
        return User.objects.all()