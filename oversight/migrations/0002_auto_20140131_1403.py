# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oversight', '0001_logentry_sensor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='current_log',
            field=models.ForeignKey(to_field=u'id', blank=True, to='oversight.LogEntry', null=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='api_endpoint',
            field=models.SlugField(unique=True),
        ),
    ]
