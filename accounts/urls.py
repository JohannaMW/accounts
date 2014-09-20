from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^home/$', 'accounting.views.home', name='home'),
    url(r'^profile/$', 'accounting.views.profile', name='profile'),
    url(r'^expenses/add$', 'accounting.views.add_expenses', name='add_expenses'),
    url(r'^expenses/$', 'accounting.views.expenses', name= 'expenses'),

    # User handling
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^register/$', 'accounting.views.register', name='register'),
    url(r'^admin/', include(admin.site.urls)),
)
