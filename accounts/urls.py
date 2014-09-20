from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^home/$', 'accounting.views.home', name='home'),
    url(r'^dashboard/$', 'accounting.views.dashboard', name='dashboard'),

    #handling expenses
    url(r'^expenses/add$', 'accounting.views.add_expenses', name='add_expenses'),
    url(r'^expenses/hist$', 'accounting.views.expenses_hist', name= 'expenses_hist'),
    url(r'^expenses/categories/$', 'accounting.views.expenses_cat', name= 'expenses_categories'),
    url(r'^expenses/categories/(?P<category_id>\w+)/$', 'accounting.views.expenses_by_cat', name= 'expenses_by_categories'),

    #handling income
    url(r'^income/add$', 'accounting.views.add_income', name='add_income'),
    url(r'^income/hist$', 'accounting.views.income_hist', name= 'income_hist'),
    url(r'^income/type/$', 'accounting.views.income_type', name= 'income_type'),
    url(r'^income/type/(?P<type_id>\w+)/$', 'accounting.views.income_by_type', name= 'income_by_type'),

    #handling savings
    url(r'^saving/add$', 'accounting.views.add_saving', name='add_saving'),

    # User handling
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^register/$', 'accounting.views.register', name='register'),
    url(r'^admin/', include(admin.site.urls)),
)
