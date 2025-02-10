from django import forms
from users.models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'date_of_birth', 'role')
