# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('oversight', '0003_sensor_log_plot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True),
        ),
    ]
