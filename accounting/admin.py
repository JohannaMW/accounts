from django.contrib import admin
from accounting.models import Expense, Category, IncomeType, Income, Saving, MonthlyExpenses, DailyExpenses, MonthlyIncome, DailyIncome

admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(IncomeType)
admin.site.register(Income)
admin.site.register(Saving)
admin.site.register(MonthlyExpenses)
admin.site.register(DailyExpenses)
admin.site.register(MonthlyIncome)
admin.site.register(DailyIncome)