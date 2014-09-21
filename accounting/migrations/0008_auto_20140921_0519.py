# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_dailyincome_monthlyincome'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dailyexpenses',
            old_name='amount',
            new_name='amount_expenses',
        ),
        migrations.RenameField(
            model_name='dailyincome',
            old_name='amount',
            new_name='amount_income',
        ),
        migrations.RenameField(
            model_name='monthlyexpenses',
            old_name='amount',
            new_name='amount_expenses',
        ),
        migrations.RenameField(
            model_name='monthlyincome',
            old_name='amount',
            new_name='amount_income',
        ),
    ]
