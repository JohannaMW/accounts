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
    category = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, related_name="dailyexpenses")

    @staticmethod
    def create_daily_expenses(day, year, month, amount, user):
        # look for existing daily expenses (overall, not affected by category)
        dailys = DailyExpenses.objects.filter(day=day, year=year, month=month, category__isnull = True)
        # no expenses for that day? --> create new one
        if not dailys:
            DailyExpenses.objects.create(year=year, month=month, day= day, amount_expenses=amount, user=user)
        else:
            # if there are already records, update them!
            for daily in dailys:
                daily.amount_expenses += amount
                daily.save()

    @staticmethod
    def create_daily_expenses_cat(day, year, month, amount, category, user):
        # look for existing daily expenses in particular category
        dailys = DailyExpenses.objects.filter(day=day, year=year, month=month, category=category)
        if not dailys:
            # no expenses in that category for that day? --> create new one
            DailyExpenses.objects.create(year=year, month=month, day=day,
                                         amount_expenses=amount, category=category, user=user)
        else:
            # if there are already records, update them!
           for daily in dailys:
                daily.amount_expenses += amount
                daily.save()

class MonthlyExpenses(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    amount_expenses = models.FloatField()
    user = models.ForeignKey(User, related_name="monthlyexpenses")
    category = models.CharField(max_length=200, blank=True, null=True)

    @staticmethod
    def create_monthly_expenses(year, month, amount, user):
        # look for existing daily expenses (overall, not affected by category)
        monthlies = MonthlyExpenses.objects.filter(month=month, year=year, category__isnull = True)
        # no expenses for that month yet? --> create new one
        if not monthlies:
            MonthlyExpenses.objects.create(year=year, month=month, amount_expenses=amount, user=user)
        else:
            # if there are already records, update them!
            for month in monthlies:
                month.amount_expenses += amount
                month.save()

    @staticmethod
    def create_monthly_expenses_cat(year, month, amount, category, user):
        # look for existing monthly expenses for that category
        monthlies = MonthlyExpenses.objects.filter(month=month, year=year, category=category)
        # no expenses for that month yet? --> create new one
        if not monthlies:
            MonthlyExpenses.objects.create(year=year, month=month, amount_expenses=amount, user=user, category=category)
        else:
            # if there are already records, update them!
            for month in monthlies:
                month.amount_expenses += amount
                month.save()

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
    type = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, related_name="dailyincome")

    @staticmethod
    def create_daily_income(day, year, month, amount, user):
        dailys = DailyIncome.objects.filter(day=day, year=year, month=month, type__isnull = True)
        if not dailys:
            DailyIncome.objects.create(year=year, month=month, day=day, amount_income=amount, user=user)
        else:
            for daily in dailys:
                daily.amount_income += amount
                daily.save()

    @staticmethod
    def create_daily_income_type(day, year, month, amount, type, user):
        dailys = DailyIncome.objects.filter(day=day, year=year, month=month, type=type)
        if not dailys:
            DailyIncome.objects.create(year=year, month=month, day=day, amount_income=amount, type=type, user=user)
        else:
           for daily in dailys:
                daily.amount_income += amount
                daily.save()

class MonthlyIncome(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    amount_income = models.FloatField()
    type = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, related_name="monthlyincome")

    @staticmethod
    def create_monthly_income(year, month, amount, user):
        monthlies = MonthlyIncome.objects.filter(month=month, year=year, type__isnull = True)
        if not monthlies:
            MonthlyIncome.objects.create(year=year, month=month, amount_income=amount, user=user)
        else:
            for month in monthlies:
                month.amount_income += amount
                month.save()

    @staticmethod
    def create_monthly_income_type(year, month, amount, type, user):
        monthlies = MonthlyIncome.objects.filter(month=month, year=year, type=type)
        if not monthlies:
            MonthlyIncome.objects.create(year=year, month=month, amount_income=amount, type=type, user=user)
        else:
           for month in monthlies:
                month.amount_income += amount
                month.save()
