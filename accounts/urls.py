from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from accounts import settings

urlpatterns = patterns('',
    url(r'^home/$', 'accounting.views.home', name='home'),
    url(r'^dashboard/$', 'accounting.views.dashboard', name='dashboard'),
    url(r'^charts/$', 'accounting.views.charts', name='charts'),

    #handling expenses
    url(r'^expenses/add$', 'accounting.views.add_expenses', name='add_expenses'),
    url(r'^expenses/hist$', 'accounting.views.expenses_hist', name= 'expenses_hist'),

    url(r'^expenses/categories/$', 'accounting.views.expenses_cat', name= 'expenses_categories'),
    url(r'^expenses/categories/(?P<category_id>\w+)/$', 'accounting.views.expenses_by_cat', name= 'expenses_by_categories'),

    # charts
    url(r'^charts/expenses/$', 'accounting.views.chart_exp', name='chart_exp'),
    url(r'^charts/expenses/choice/month/$', 'accounting.views.chart_exp_choice_month', name='chart_exp_choice_month'),
    url(r'^charts/expenses/choice/year/$', 'accounting.views.chart_exp_choice_year', name='chart_exp_choice_year'),
    url(r'^charts/expenses/choice/relations/$', 'accounting.views.chart_exp_choice_relation', name='chart_exp_choice_relation'),

    url(r'^charts/expenses/(?P<year>\w+)/$', 'accounting.views.chart_exp_year', name='chart_exp_year'),
    url(r'^charts/expenses/(?P<year>\w+)/(?P<category>\w+)/$', 'accounting.views.chart_exp_year_cat', name='chart_exp_year_cat'),
    url(r'^charts/expense/categories/(?P<year>\w+)/$', 'accounting.views.chart_spendings_categories', name='chart_spendings_categories'),
    url(r'^charts/expense/categories/(?P<year>\w+)/(?P<month>\w+)/$', 'accounting.views.chart_spendings_categories_month', name='chart_spendings_categories_month'),
    url(r'^charts/expense/(?P<year>\w+)/(?P<month>\w+)/$', 'accounting.views.chart_exp_month', name='chart_exp_month'),
    url(r'^charts/expense/(?P<year>\w+)/(?P<month>\w+)/(?P<category>\w+)/$', 'accounting.views.chart_exp_month_cat', name='chart_exp_month_cat'),

# charts
    url(r'^charts/income/$', 'accounting.views.chart_inc', name='chart_inc'),
    url(r'^charts/income/choice/month/$', 'accounting.views.chart_inc_choice_month', name='chart_inc_choice_month'),
    url(r'^charts/income/choice/year/$', 'accounting.views.chart_inc_choice_year', name='chart_inc_choice_year'),
    url(r'^charts/income/choice/relations/$', 'accounting.views.chart_inc_choice_relation', name='chart_inc_choice_relation'),
    url(r'^charts/income/(?P<year>\w+)/$', 'accounting.views.chart_inc_year', name='chart_inc_year'),
    url(r'^charts/income/(?P<year>\w+)/(?P<month>\w+)/$', 'accounting.views.chart_inc_month', name='chart_inc_month'),

    url(r'^income/(?P<type>\w+)/(?P<year>\w+)/$', 'accounting.views.chart_income_type_year', name='chart_income_type_year'),
    url(r'^income/(?P<type>\w+)/(?P<year>\w+)/(?P<month>\w+)/$', 'accounting.views.chart_income_type_month', name='chart_income_type_month'),

    url(r'^charts/incomes/types/(?P<year>\w+)/$', 'accounting.views.chart_income_type', name='chart_income_types'),
    url(r'^charts/incomes/types/(?P<year>\w+)/(?P<month>\w+)/$', 'accounting.views.chart_incomes_type_month', name='chart_income_types_month'),


    #handling income
    url(r'^income/add$', 'accounting.views.add_income', name='add_income'),
    url(r'^income/hist$', 'accounting.views.income_hist', name= 'income_hist'),
    url(r'^income/type/$', 'accounting.views.income_type', name= 'income_type'),
    url(r'^income/type/(?P<type_id>\w+)/$', 'accounting.views.income_by_type', name= 'income_by_type'),

    #Charts
    url(r'^charts/cashflow/$', 'accounting.views.chart_cashflow_choice', name='chart_cashflow_choice'),
    url(r'^charts/cashflow/(?P<year>\w+)/$', 'accounting.views.chart_cashflow_year', name='chart_cashflow_year'),
    url(r'^charts/cashflow/(?P<year>\w+)/(?P<month>\w+)/$', 'accounting.views.chart_cashflow_month', name='chart_cashflow_month'),
    # User handling
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^register/$', 'accounting.views.register', name='register'),
    url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
