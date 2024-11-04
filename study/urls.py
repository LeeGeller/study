from django.urls import path

from study.apps import StudyConfig
from study.views import HomeListView

appname = StudyConfig.name
urlpatterns = [
    path('', HomeListView.as_view(template_name='study/index/html'), name='home'),

]
