__author__ = 'johanna'
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from accounting.models import Expense, Saving, IncomeType, Income

class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ExpenseForm(ModelForm):

     class Meta:
         model = Expense



