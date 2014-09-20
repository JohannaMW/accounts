from django.contrib import admin
from accounting.models import Expense, Category, IncomeType, Income, Saving

admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(IncomeType)
admin.site.register(Income)
admin.site.register(Saving)