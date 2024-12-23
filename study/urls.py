from django.urls import path

from study.apps import StudyConfig
from study.views import HomeListView, TestsListView, TestsCreateView, TestsDeleteView, TestsDetailView

appname = StudyConfig.name
urlpatterns = [
    path('', HomeListView.as_view(template_name='study/home.html'), name='home'),
    path('tests/', TestsListView.as_view(), name='tests_list'),
    path('test_create/', TestsCreateView.as_view(), name='test_form'),
    path('test/<int:pk>/delete/', TestsDeleteView.as_view(), name='test_delete'),
    path('test/<int:pk>/detail/', TestsDetailView.as_view(), name='test_detail'),

]
