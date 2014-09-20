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

class Saving(models.Model):
    title = models.CharField(max_length=120)
    amount = models.FloatField()
    from_date = models.DateField()
    to_date = models.DateField()
    user = models.ForeignKey(User, related_name="savings")

    def __unicode__(self):
        return self.title