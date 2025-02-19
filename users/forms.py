from django import forms
from django.contrib.auth.models import Group

from users.models import User


class UserCreationForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Group.objects.all(), label='Роль', empty_label='Выберите роль',
                                  required=True)

    password = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'id_password'}),
                               required=False, label='Пароль')

    class Meta:
        model = User
        fields = ('username', 'date_of_birth', 'role', 'password')
