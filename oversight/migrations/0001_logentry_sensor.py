# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oversight', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='sensor',
            field=models.ForeignKey(to='oversight.Sensor', to_field=u'id', default=0),
            preserve_default=False,
        ),
    ]
