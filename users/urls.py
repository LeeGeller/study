from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path
from django.views.generic import RedirectView

from studyplatform import settings
from users.apps import UsersConfig
from users.views import UsersListView, UsersCreateView, generate_password_view, UsersDeleteView, UsersDetailsView, \
    UsersUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    re_path(r'^accounts/login/$', RedirectView.as_view(url='/login/', permanent=False)),
    path('user_list/', UsersListView.as_view(), name='users'),
    path('user_create/', UsersCreateView.as_view(), name='create_users'),
    path('<int:pk>/edit/', UsersUpdateView.as_view(), name='update_users'),
    path('generate_password/', generate_password_view, name='generate_password'),
    path('<int:pk>/user_delete/', UsersDeleteView.as_view(), name='delete_user'),
    path('<int:pk>/', UsersDetailsView.as_view(), name='detail_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
