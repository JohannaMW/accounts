# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0008_auto_20140921_0519'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyincome',
            name='type',
            field=models.CharField(default='chash', max_length=200),
            preserve_default=False,
        ),
    ]
