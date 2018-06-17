from django.conf.urls import url
from NNModelManager import views

urlpatterns = [
    url(r'^NNModelHome/$', views.index),
    url(r'^config/$', views.model_config),
]
