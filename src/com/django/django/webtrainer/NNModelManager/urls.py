from django.conf.urls import url
from NNModelManager import views

urlpatterns = [
    url(r'^NNModelHome/$', views.index),
    url(r'^dataManage/$', views.dataManage),
    url(r'^Operations/$', views.operations),
]
