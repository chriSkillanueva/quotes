from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^contribute$', views.contribute),
    url(r'^addfav/(?P<quote_id>\d+)$', views.addfav),
    url(r'^removefav/(?P<quote_id>\d+)$', views.removefav),
    url(r'^users/(?P<user_id>\d+)$', views.userpage)
]
