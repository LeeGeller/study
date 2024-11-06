from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path
from django.views.generic import RedirectView

from studyplatform import settings
from users.apps import UsersConfig

appname = UsersConfig.name
urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    re_path(r'^accounts/login/$', RedirectView.as_view(url='/login/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
