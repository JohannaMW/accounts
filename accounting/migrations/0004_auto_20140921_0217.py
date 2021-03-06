# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_dailyexpenses'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyexpenses',
            name='month',
            field=models.IntegerField(default=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailyexpenses',
            name='year',
            field=models.IntegerField(default=2014),
            preserve_default=False,
        ),
    ]
