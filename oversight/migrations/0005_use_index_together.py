# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('oversight', '0004_add_dbindex_to_logentry_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterIndexTogether(
            name='logentry',
            index_together=set([(b'sensor', b'datetime')]),
        ),
    ]
