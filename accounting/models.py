from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=120)

    def __unicode__(self):
        return self.name

class Expense(models.Model):
    name = models.CharField(max_length=120)
    amount = models.FloatField()
    date = models.DateField()
    category = models.ForeignKey(Category, related_name="expenses")
    user = models.ForeignKey(User, related_name="expenses")
    fix = models.BooleanField(default=False)
    variable = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class DailyExpenses(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    amount_expenses = models.FloatField()
    user = models.ForeignKey(User, related_name="dailyexpenses")

    @staticmethod
    def create_daily_expenses(year, month, user):
        day = 1
        while day <= 31:
            # get all expenses for the day
            day_expenses = Expense.objects.filter(date__year=year, date__month=month, date__day=day,
                               user=user)
            amount = 0
            # add expenses of the day together
            for expense in day_expenses:
                amount += expense.amount
            DailyExpenses.objects.create(year=year, month=month, day= day, amount_expenses=amount, user=user)
            day += 1

class MonthlyExpenses(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    amount_expenses = models.FloatField()
    user = models.ForeignKey(User, related_name="monthlyexpenses")

    @staticmethod
    def create_monthly_expenses(year, user):
        month = 1
        while month <= 12:
            # get all expenses for the month
            month_expenses = Expense.objects.filter(date__year=year, date__month=month,
                                   user=user)
            amount = 0
            # add expenses of the day together
            for expense in month_expenses:
                    amount += expense.amount
            MonthlyExpenses.objects.create(year=year, month=month, amount_expenses=amount, user=user)
            month += 1

class IncomeType(models.Model):
    name = models.CharField(max_length=120)
    exchange_rate = models.FloatField()

    def __unicode__(self):
        return self.name

class Income(models.Model):
    name = models.CharField(max_length=120)
    amount = models.FloatField()
    date = models.DateField()
    type = models.ForeignKey(IncomeType, related_name="income")
    user = models.ForeignKey(User, related_name="income")

    def __unicode__(self):
        return self.name

class DailyIncome(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    amount_income = models.FloatField()
    user = models.ForeignKey(User, related_name="dailyincome")

    @staticmethod
    def create_daily_income(year, month, user):
        day = 1
        while day <= 31:
            # get all expenses for the day
            day_income = Income.objects.filter(date__year=year, date__month=month, date__day=day,
                               user=user)
            amount = 0
            # add expenses of the day together
            for income in day_income:
                amount += income.amount
            DailyIncome.objects.create(year=year, month=month, day= day, amount_income=amount, user=user)
            day += 1

class MonthlyIncome(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    amount_income = models.FloatField()
    user = models.ForeignKey(User, related_name="monthlyincome")

    @staticmethod
    def create_monthly_income(year, user):
        month = 1
        while month <= 12:
            # get all expenses for the month
            month_incomes = Income.objects.filter(date__year=year, date__month=month,
                               user=user)
            amount = 0
            # add expenses of the day together
            for income in month_incomes:
                amount += income.amount
            MonthlyIncome.objects.create(year=year, month=month, amount_income=amount, user=user)
            month += 1

class Saving(models.Model):
    title = models.CharField(max_length=120)
    amount = models.FloatField()
    from_date = models.DateField()
    to_date = models.DateField()
    user = models.ForeignKey(User, related_name="savings")

    def __unicode__(self):
        return self.title