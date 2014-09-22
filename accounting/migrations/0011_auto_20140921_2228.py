# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0010_auto_20140921_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saving',
            name='user',
        ),
        migrations.DeleteModel(
            name='Saving',
        ),
        migrations.AddField(
            model_name='dailyexpenses',
            name='category',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlyexpenses',
            name='category',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlyincome',
            name='type',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
