# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_dailyincome_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyincome',
            name='type',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
