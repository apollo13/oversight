# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oversight', '0002_auto_20140131_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='log_plot',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
