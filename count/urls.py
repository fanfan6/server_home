<<<<<<< HEAD
# coding=utf-8

from django.conf.urls import url
from count import views

urlpatterns = [
    url(r'^count_info?.*$', views.count_info),
    url(r'^search$', views.counts),
    url(r'^download$', views.count_download),
=======
# coding=utf-8

from django.conf.urls import url
from count import views

urlpatterns = [
    url(r'^count_info?.*$', views.count_info),
    url(r'^search$', views.counts),
    url(r'^download$', views.count_download),
>>>>>>> de3dd54b5b842fdf8945198b6bc0388571d1e684
]