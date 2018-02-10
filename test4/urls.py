from django.conf.urls import url, include

from test4 import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^add', views.add),
]