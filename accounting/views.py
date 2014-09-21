from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounting.forms import EmailUserCreationForm, ExpenseForm, IncomeForm, SavingForm
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login
from accounting.models import Expense, Income, IncomeType, Saving, Category
import datetime
from chartit import DataPool, Chart

def home(request):
    return render(request, 'home.html', {})

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
            if form.save():
                return redirect("/expenses/hist/")
    else:
        form = ExpenseForm()
    data = {'form': form}
    return render(request, 'Expenses/add_expenses.html', data)

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
            if form.save():
                return redirect("/home/")
    else:
        form = IncomeForm()
    data = {'form': form}
    return render(request, 'Income/add_income.html', data)

@login_required
def add_saving(request):
    # lets user add a saving plan
    if request.method == "POST":
        form = SavingForm(request.POST)
        if form.is_valid():
            if form.save():
                return redirect("/home/")
    else:
        form = SavingForm()
    data = {'form': form}
    return render(request, 'Saving/add_saving.html', data)

@login_required
def saving_plans(request):
    # lists all saving plans
    plans = Saving.objects.filter(user=request.user).order_by('-from_date')
    return render(request, 'Saving/saving_plans.html', {'plans': plans})

@login_required
def chart_exp_month(request):
    # creates a chart of monthly spendings
    #Step 1: Create a DataPool with the data we want to retrieve.
    month = datetime.date.today().month
    expensedata = \
        DataPool(
           series=
            [{'options': {
               'source': Expense.objects.filter(date__month=month,
                           user=request.user)},
              'terms': [
                'date',
                'amount']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = expensedata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'date': [
                    'amount']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Expenses in {}'.format(month)},
               'xAxis': {
                    'title': {
                       'text': 'Date'}}})

    #Step 3: Send the chart object to the template.
    return render(request, "Charts/chart_exp_month.html", {'expensechart': cht})