__author__ = 'johanna'
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from accounting.models import Expense, IncomeType, Income

class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ExpenseForm(ModelForm):

     class Meta:
         model = Expense

class IncomeForm(ModelForm):

     class Meta:
         model = Income

class YearForm(forms.Form):
    year = forms.IntegerField(required=False)

class YearMonthForm(forms.Form):
    year = forms.IntegerField(required=False)
    month = forms.IntegerField(required=False)
