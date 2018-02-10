from django.conf.urls import url

from statistics import views


urlpatterns = [
    url(r'^index$', views.index),
    url(r'^add$', views.add),
    url(r'^static_info$', views.static_info),
    url(r'^app_pass$', views.app_pass),
    url(r'^mod_grade', views.mod_grade),
]
