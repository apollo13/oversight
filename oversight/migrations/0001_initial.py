# encoding: utf8
from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('api_endpoint', models.SlugField()),
                ('unit', models.CharField(max_length=255)),
                ('sensor_class', models.CharField(max_length=255)),
                ('params', models.TextField()),
                ('current_log', models.ForeignKey(to='oversight.LogEntry', to_field=u'id', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
