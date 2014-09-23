from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounting.forms import EmailUserCreationForm, ExpenseForm, IncomeForm, YearForm, YearMonthForm
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login
from accounting.models import Expense, Income, IncomeType, Category, DailyExpenses, MonthlyExpenses, DailyIncome, MonthlyIncome
import datetime
from chartit import DataPool, Chart, PivotDataPool, PivotChart
from django.db.models import Sum

def home(request):
    return render(request, 'home.html', {})

def charts(request):
    return render(request, 'Charts/charts.html', {})

@login_required
def dashboard(request):
    month = datetime.date.today().month
    incomes = Income.objects.filter(date__month=month,
                           user=request.user)
    total_income = 0
    for income in incomes:
        total_income += income.amount
    expenses = Expense.objects.filter(date__month=month,
                           user=request.user)
    total_expenses = 0
    for expense in expenses:
        total_expenses += expense.amount
    total = total_income - total_expenses
    data = {"total_income" : total_income, "total_expenses" : total_expenses, "total" : total}
    return render(request, "dashboard.html", data)

def register(request):
    # let's user register
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password1"]
            user = form.save()
            text_content = 'Thank you for signing up for our website on {}, {} ' \
                           '{}'.format(user.first_name, user.last_name, user.date_joined)
            html_content = '<h2>Thanks {} {} for signing up! {}</h2> <div>I hope you enjoy using ' \
                           'our site</div>'.format(user.first_name, user.last_name, user.date_joined)
            msg = EmailMultiAlternatives("Welcome!", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect("/dashboard/")
    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })

@login_required
def expenses_hist(request):
    # lists expenses historically
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'Expenses/expenses_historical.html', {'expenses': expenses})

@login_required
def expenses_by_cat(request, category_id):
    # lists expenses by category
    category = Category.objects.get(id=category_id)
    expenses = Expense.objects.filter(user=request.user, category__id=category_id)
    return render(request, 'Expenses/expenses_by_category.html', {'expenses': expenses, 'category' : category})

@login_required
def expenses_cat(request):
    # lists all available categories
    categories = Category.objects.all()
    return render(request, 'Expenses/expenses_categories.html', {'categories': categories})


@login_required
def add_expenses(request):
    # lets user add an expense
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            new_expense = form.save()
            month = new_expense.date.month
            year = new_expense.date.year
            day = new_expense.date.day
            amount = new_expense.amount
            category = new_expense.category
            # update monthly and daily records
            DailyExpenses.create_daily_expenses(year=year, month=month, day=day, amount=amount, user=request.user)
            DailyExpenses.create_daily_expenses_cat(year=year, month=month, day=day, amount=amount, category=category, user=request.user)
            MonthlyExpenses.create_monthly_expenses(year=year, month=month, amount=amount, user=request.user)
            MonthlyExpenses.create_monthly_expenses_cat(year=year, month=month, amount=amount, category=category, user=request.user)
            return redirect("/expenses/hist")
    else:
        form = ExpenseForm()
    data = {'form': form}
    return render(request, 'Expenses/add_expenses.html', data)

@login_required
def chart_income_type_month(request, type, year, month):
    form = YearMonthForm(request.POST)
    if request.method == 'POST':
        form = YearMonthForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            month=form.cleaned_data['month']
            return redirect("/charts/income/{}/{}/{}".format(type, year, month))
    incomedata = \
        DataPool(
           series=
            [{'options': {'source': DailyIncome.objects.filter(month=month, year=year, type=type,
                           user=request.user)}, 'terms': ['day', 'amount_income']}])
    cht = Chart(
            datasource = incomedata,
            series_options =
              [{'options':{ 'type': 'line', 'stacking': False},
                'terms':{'day': ['amount_income']}}],
            chart_options =
              {'title': {'text': '{} incomes in {}.{}'.format(type, month, year)},
               'xAxis': {'title': {'text': 'Day'}}})
    return render(request, "Charts/chart_inc_type_month.html", {'incomecharttype': cht, "form":form})

@login_required
def chart_inc_month(request, year, month):
    form = YearMonthForm(request.POST)
    if request.method == 'POST':
        form = YearMonthForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            month=form.cleaned_data['month']
            return redirect("/charts/income/{}/{}".format(year, month))
    incomedata = \
        DataPool(
           series=
            [{'options': {'source': DailyIncome.objects.filter(month=month, year=year, type__isnull=True,
                           user=request.user)}, 'terms': ['day', 'amount_income']}])
    cht = Chart(
            datasource = incomedata,
            series_options =
              [{'options':{ 'type': 'line', 'stacking': False},
                'terms':{'day': ['amount_income']}}],
            chart_options =
              {'title': {'text': 'Incomes in {}.{}'.format(month,year)},
               'xAxis': {'title': {'text': 'Day'}}})
    return render(request, "Charts/chart_inc_month.html", {'incomechart': cht, 'form':form})

@login_required
def chart_income_type_year(request, type, year):
    form = YearForm(request.POST)
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            return redirect("/charts/income/{}/{}".format(type, year))
    incomedata = \
        DataPool(
           series=
            [{'options': {'source': MonthlyIncome.objects.filter(year=year, user=request.user, type=type)},
              'terms': ['month', 'amount_income']}])

    cht = Chart(
            datasource = incomedata,
            series_options = [{'options':{'type': 'line', 'stacking': False},
                'terms':{'month': ['amount_income']}}],
            chart_options = {'title': {'text': '{} income in {}'.format(type, year)},
               'xAxis': {'title': {'text': 'Month'}}})

    return render(request, "Charts/chart_inc_type_year.html", {'incomechartyear_type': cht, 'form' : form})

@login_required
def chart_inc_year(request, year):
    form = YearForm(request.POST)
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            return redirect("/charts/income/{}".format(year))
    incomedata = \
        DataPool(
           series=
            [{'options': {'source': MonthlyIncome.objects.filter(year=year, user=request.user, type__isnull=True)},
              'terms': ['month', 'amount_income']}])

    cht = Chart(
            datasource = incomedata,
            series_options = [{'options':{'type': 'line', 'stacking': False},
                'terms':{'month': ['amount_income']}}],
            chart_options = {'title': {'text': 'Income in {}'.format(year)},
               'xAxis': {'title': {'text': 'Month'}}})

    return render(request, "Charts/chart_inc_year.html", {'incomechartyear': cht, 'form' : form})

@login_required
def income_hist(request):
    # lists expenses historically
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'Income/income_historical.html', {'incomes': incomes})

@login_required
def income_type(request):
    # lists all available categories
    types = IncomeType.objects.all()
    return render(request, 'Income/income_types.html', {'types': types})

@login_required
def income_by_type(request, type_id):
    # lists expenses by category
    type = IncomeType.objects.get(id=type_id)
    incomes = Income.objects.filter(user=request.user, type__id=type_id)
    return render(request, 'Income/income_by_type.html', {'incomes': incomes, 'type' : type})

@login_required
def add_income(request):
    # lets user add an income
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            new_income = form.save()
            month = new_income.date.month
            year = new_income.date.year
            day = new_income.date.day
            amount = new_income.amount
            type = new_income.type
            # update monthly/ daily records
            DailyIncome.create_daily_income(year=year, month=month, day=day, amount=amount, user=request.user)
            DailyIncome.create_daily_income_type(year=year, month=month, day=day, amount=amount, type=type, user=request.user)
            MonthlyIncome.create_monthly_income(year=year, month=month, amount=amount, user=request.user)
            MonthlyIncome.create_monthly_income_type(year=year, month=month, amount=amount, type=type, user=request.user)
            return redirect("/income/hist")
    else:
        form = IncomeForm()
    data = {'form': form}
    return render(request, 'Income/add_income.html', data)

def chart_exp(request):
    today = datetime.date.today()
    month = today.month
    expenses = Expense.objects.filter(user=request.user, date__month=month)
    return render(request, 'Charts/chart_exp.html', {'expenses': expenses, 'month' : month})

def chart_exp_choice(request):
    today = datetime.date.today()
    month = today.month
    year = today.year
    return render(request, 'Charts/chart_exp_choice.html', {'month' : month, 'year':year})

def chart_inc_choice(request):
    today = datetime.date.today()
    month = today.month
    year = today.year
    return render(request, 'Charts/chart_inc_choice.html', {'month' : month, 'year':year})

def chart_cashflow_choice(request):
    today = datetime.date.today()
    month = today.month
    year = today.year
    return render(request, 'Charts/chart_cashflow.html', {'month' : month, 'year':year})


def chart_inc(request):
    today = datetime.date.today()
    month = today.month
    incomes = Income.objects.filter(user=request.user, date__month=month)
    return render(request, 'Charts/chart_inc.html', {'incomes': incomes, 'month' : month})

@login_required
def chart_exp_month_cat(request, year, month, category):
    form = YearMonthForm(request.POST)
    if request.method == 'POST':
        form = YearMonthForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            month=form.cleaned_data['month']
            return redirect("/charts/expense/{}/{}/{}".format(year, month, category))
    expensedata = \
        DataPool(series=[
            {'options': {'source': DailyExpenses.objects.filter(month=month, year=year, user=request.user, category=category)},
              'terms': ['day','amount_expenses']}])
    cht = Chart(
            datasource = expensedata,
            series_options = [{'options':{ 'type': 'line', 'stacking': False}, 'terms':{'day': ['amount_expenses']}}],
            chart_options = {'title': {'text': 'Expenses in {}, {}.{}'.format(category, month, year)},
               'xAxis': {'title': {'text': 'Day'}}})
    return render(request, "Charts/chart_exp_month_cat.html", {'expensechart_percat': cht, 'form':form})

@login_required
def chart_exp_month(request, year, month):
    form = YearMonthForm(request.POST)
    if request.method == 'POST':
        form = YearMonthForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            month=form.cleaned_data['month']
            return redirect("/charts/expense/{}/{}".format(year, month))
    expensedata = \
        DataPool(series=[
            {'options': {'source': DailyExpenses.objects.filter(month=month, year=year, user=request.user, category__isnull=True)},
              'terms': ['day','amount_expenses']}])
    cht = Chart(
            datasource = expensedata,
            series_options = [{'options':{ 'type': 'line', 'stacking': False}, 'terms':{'day': ['amount_expenses']}}],
            chart_options = {'title': {'text': 'Expenses in {}.{}'.format(month, year)},
               'xAxis': {'title': {'text': 'Day'}}})
    return render(request, "Charts/chart_exp_month.html", {'expensechart': cht, 'form':form})

@login_required
def chart_exp_year(request, year):
    form = YearForm(request.POST)
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            return redirect("/charts/expenses/{}".format(year))
    expensedata = \
        DataPool(series= [{'options': {'source': MonthlyExpenses.objects.filter(year=year, category__isnull=True, user=request.user)},
              'terms': ['month','amount_expenses']}])
    cht = Chart(
            datasource = expensedata,
            series_options = [{'options':{'type': 'line', 'stacking': False}, 'terms':{'month': ['amount_expenses']}}],
            chart_options =
              {'title': {'text': 'Expenses in {}'.format(year)}, 'xAxis': {'title': {'text': 'Month'}}})

    return render(request, "Charts/chart_exp_year.html", {'expensechartyear': cht, 'form':form})

@login_required
def chart_exp_year_cat(request, year, category):
    form = YearForm(request.POST)
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            return redirect("/charts/expenses/{}/{}".format(year, category))
    expensedata = \
        DataPool(series= [{'options': {'source': MonthlyExpenses.objects.filter(year=year, category=category, user=request.user)},
              'terms': ['month','amount_expenses']}])
    cht = Chart(
            datasource = expensedata,
            series_options = [{'options':{'type': 'line', 'stacking': False}, 'terms':{'month': ['amount_expenses']}}],
            chart_options =
              {'title': {'text': 'Expenses in {}, {}'.format(category, year)}, 'xAxis': {'title': {'text': 'Month'}}})

    return render(request, "Charts/chart_exp_year_cat.html", {'expensechartyear_percat': cht, 'form':form})

def chart_cashflow_year(request, year):
    form = YearForm(request.POST)
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            return redirect("/charts/cashflow/{}".format(year))
    ds = DataPool(
           series=
            [{'options': {'source': MonthlyIncome.objects.filter(year=year,
                           user=request.user, type__isnull=True)},
              'terms': ['month', 'amount_income']},
             {'options': {'source': MonthlyExpenses.objects.filter(year=year, category__isnull=True,
                           user=request.user)},
              'terms': [{'month_expenses' : 'month'},'amount_expenses']}])

    cht = Chart(
            datasource = ds,
            series_options =
              [{'options':{'color': '#51D65C', 'type': 'area','stacking': False},
                'terms':{'month': ['amount_income']}},
               {'options':{'color': '#D44C6C', 'type': 'area','stacking': False},
                'terms':{'month_expenses': ['amount_expenses']}}],

            chart_options =
              {'title': {'text': 'Cash Flow {}'.format(year)},
               'xAxis': {'title': {'text': 'Month'}}})
    return render(request, "Charts/chart_cashflow_year.html", {'cashflowchartyear': cht, 'form':form})

def chart_cashflow_month(request, year, month):
    ds = DataPool(
           series=
            [{'options': {'source': DailyExpenses.objects.filter(year=year, month=month, category__isnull=True,
                           user=request.user)},
              'terms': [{'day_expenses' : 'day'},'amount_expenses']},
             {'options': {'source': DailyIncome.objects.filter(year=year, month=month, type__isnull=True,
                           user=request.user)},
              'terms': ['day', 'amount_income']}])

    cht = Chart(
            datasource = ds,
            series_options =
              [{'options':{'color': '#D44C6C', 'type': 'area','stacking': False},
                'terms':{'day_expenses': ['amount_expenses']}},
               {'options':{'color': '#51D65C', 'type': 'area','stacking': False},
                'terms':{'day': ['amount_income']}}],

            chart_options =
              {'title': {'text': 'Cash Flow {}'.format(month)},
               'xAxis': {'title': {'text': 'Day'}}})
    return render(request, "Charts/chart_cashflow_day.html", {'cashflowchartday': cht})

def chart_spendings_categories(request, year):
    form = YearForm(request.POST)
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            return redirect("/charts/expense/categories/{}".format(year))
    ds = PivotDataPool( series= [
       {'options':{ 'source': Expense.objects.filter(date__year=year),
          'categories': 'category__name'},
        'terms': {'tot_exp':Sum('amount')}}])
    pivcht = PivotChart(
          datasource = ds,
          series_options = [ {'options': {'type': 'column'}, 'terms': ['tot_exp']}],
          chart_options = {'title': {'text':'Expenses by Category {}'.format(year)}})
    return render(request, "Charts/chart_spendings_categories.html", {'spendingchartcat': pivcht, 'form' :form})

def chart_spendings_categories_month(request, year, month):
    form = YearMonthForm(request.POST)
    if request.method == 'POST':
        form = YearMonthForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            month=form.cleaned_data['month']
            return redirect("/charts/expense/categories/{}/{}".format(year, month))
    ds = PivotDataPool( series= [
       {'options':{ 'source': Expense.objects.filter(date__year=year, date__month=month),
          'categories': 'category__name'},
        'terms': {'tot_exp':Sum('amount')}}])
    pivcht = PivotChart(
          datasource = ds,
          series_options = [ {'options': {'type': 'column'}, 'terms': ['tot_exp']}],
          chart_options = {'title': {'text':'Expenses by Category {}.0{}'.format(year, month)}})
    return render(request, "Charts/chart_spendings_categories_month.html", {'spendingchartcat_month': pivcht, 'form':form})

def chart_income_type(request, year):
    form = YearForm(request.POST)
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            return redirect("/charts/incomes/types/{}".format(year))
    ds = PivotDataPool( series= [
       {'options':{ 'source': Income.objects.filter(date__year=year),
          'categories': 'type__name'},
        'terms': {'tot_inc':Sum('amount')}}])
    pivcht = PivotChart(
          datasource = ds,
          series_options = [ {'options': {'type': 'column'}, 'terms': ['tot_inc']}],
          chart_options = {'title': {'text':'Income by Type, {}'.format(year)}})
    return render(request, "Charts/chart_income_type.html", {'incomecharttype': pivcht, "form":form})

def chart_incomes_type_month(request, year, month):
    form = YearMonthForm(request.POST)
    if request.method == 'POST':
        form = YearMonthForm(request.POST)
        if form.is_valid():
            year=form.cleaned_data['year']
            month=form.cleaned_data['month']
            return redirect("/charts/income/types/{}/{}".format(year, month))
    ds = PivotDataPool( series= [
       {'options':{ 'source': Income.objects.filter(date__year=year, date__month=month),
          'categories': 'type__name'},
        'terms': {'tot_inc':Sum('amount')}}])
    pivcht = PivotChart(
          datasource = ds,
          series_options = [ {'options': {'type': 'column'}, 'terms': ['tot_inc']}],
          chart_options = {'title': {'text':'Income by Type {}.{}'.format(year, month)}})
    return render(request, "Charts/chart_income_type_month.html", {'incomecharttype_month': pivcht, 'form':form})

