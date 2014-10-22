# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oversight', '0006_add_logging_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='alarm_above',
            field=models.CharField(default='', max_length=255, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensor',
            name='alarm_acked',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sensor',
            name='alarm_below',
            field=models.CharField(default='', max_length=255, blank=True),
            preserve_default=False,
        ),
    ]
