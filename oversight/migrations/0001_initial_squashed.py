# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [(b'oversight', '0001_initial'), (b'oversight', '0001_logentry_sensor'), (b'oversight', '0002_auto_20140131_1403'), (b'oversight', '0003_sensor_log_plot'), (b'oversight', '0004_add_dbindex_to_logentry_datetime'), (b'oversight', '0005_use_index_together'), (b'oversight', '0006_add_logging_field'), (b'oversight', '0007_add_alaram_fields')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'datetime', models.DateTimeField(default=django.utils.timezone.now)),
                (b'value', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(max_length=255)),
                (b'api_endpoint', models.SlugField(unique=True)),
                (b'unit', models.CharField(max_length=255)),
                (b'sensor_class', models.CharField(max_length=255)),
                (b'params', models.TextField()),
                (b'current_log', models.ForeignKey(related_name='+', blank=True, to='oversight.LogEntry', null=True)),
                (b'log_plot', models.BooleanField(default=False)),
                ('logging_enabled', models.BooleanField(default=True)),
                ('alarm_above', models.CharField(default='', max_length=255, blank=True)),
                ('alarm_acked', models.BooleanField(default=True)),
                ('alarm_below', models.CharField(default='', max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name=b'logentry',
            name=b'sensor',
            field=models.ForeignKey(to=b'oversight.Sensor', default=0, to_field='id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='logentry',
            index_together=set([(b'sensor', b'datetime')]),
        ),
    ]
