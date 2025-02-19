from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    role = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name="Роль", null=True, blank=True,
                             related_name="user_role")
    date_of_birth = models.DateField(verbose_name="Дата рождения", blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
