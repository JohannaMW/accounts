# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20140919_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='fix',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expense',
            name='variable',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
