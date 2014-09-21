# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0004_auto_20140921_0217'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyexpenses',
            name='user',
            field=models.ForeignKey(related_name=b'dailyexpenses', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
