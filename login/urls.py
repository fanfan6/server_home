from django.conf.urls import url, include

from views import LoginView, index, logout


urlpatterns = [
    url(r'^login', LoginView.as_view()),
    url(r'^logout', logout),
    url(r'', index),
]
