# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oversight', '0005_use_index_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='logging_enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensor',
            name=b'current_log',
            field=models.ForeignKey(related_name='+', blank=True, to='oversight.LogEntry', null=True),
            preserve_default=True,
        ),
    ]
