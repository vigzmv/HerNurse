from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from App.forms import LoginForm
from App.views import register

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('App.urls')),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
    url(r'^register/$', register, name="register"),
]