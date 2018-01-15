from django.conf.urls import url, include

from report_info import views


urlpatterns = [
    url(r'^report/(?P<nid>\d+)', views.report),
    url(r'^service$', views.service),
    url(r'^search$', views.search),
    url(r'^search_info$', views.search_info),
]
