from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create_user(
            username='AdminOlimpbet'
        )
        user.set_password('12345')
        user.save()