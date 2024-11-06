from django.views.generic import ListView

from study.models import Tests


class HomeListView(LoginRequiredMixin, ListView):
    model = Tests

    def get_queryset(self):
        return Tests.objects.filter(is_active=True)
