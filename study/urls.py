from django.urls import path

from study.apps import StudyConfig
from study.views import HomeListView, TestsListView

appname = StudyConfig.name
urlpatterns = [
    path('', HomeListView.as_view(template_name='study/home.html'), name='home'),
    path('tests/', TestsListView.as_view(), name='tests_list')

]
