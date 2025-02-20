from django import forms
from django.contrib.auth.models import Group

from users.models import User


class UserCreationForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label='Роль',
        empty_label='Выберите роль',
        required=True, widget=forms.Select()
    )

    password = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'id_password'}),
        required=False, label='Пароль')

    class Meta:
        model = User
        fields = ('username', 'date_of_birth', 'role', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        group = self.cleaned_data.get('role')

        if commit:
            user.save()
            user.groups.clear()
            user.groups.set([group])

        return user


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'id_password'}),
                               label="Новый пароль")

    class Meta:
        model = User
        fields = ('username', 'date_of_birth', 'role')

        def save(self, commit=False):
            user = super().save(commit=False)
            if self.cleaned_data.get('password'):
                user.set_password(self.cleaned_data.get('password'))

            if self.cleaned_data.get('role'):
                user.groups.clear()
                user.groups.set([self.cleaned_data.get('role')])

            if commit:
                user.save()
            return user
