from django.conf.urls import url, include

from report_info import views


urlpatterns = [
    url(r'^report/(?P<nid>\d+)', views.report),
    url(r'^service_info$', views.service_info),
    url(r'^service_user$', views.service_user),
    url(r'^search$', views.search),
    url(r'^search_info$', views.search_info),
    url(r'^history$', views.report_history),
]
