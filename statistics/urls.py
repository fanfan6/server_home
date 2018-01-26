from django.conf.urls import url

from statistics import views


urlpatterns = [
    url(r'^index$', views.index),
]
