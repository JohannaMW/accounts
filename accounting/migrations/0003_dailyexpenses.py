# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_monthlyexpenses'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyExpenses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.IntegerField()),
                ('amount', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
