import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = []

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("datetime", models.DateTimeField(default=django.utils.timezone.now)),
                ("value", models.CharField(max_length=255)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Sensor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("api_endpoint", models.SlugField(unique=True)),
                ("unit", models.CharField(max_length=255)),
                ("sensor_class", models.CharField(max_length=255)),
                ("params", models.TextField()),
                (
                    "current_log",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="oversight.LogEntry",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                ("log_plot", models.BooleanField(default=False)),
                ("logging_enabled", models.BooleanField(default=True)),
                ("alarm_above", models.CharField(max_length=255, blank=True)),
                ("alarm_acked", models.BooleanField(default=True)),
                ("alarm_below", models.CharField(max_length=255, blank=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="logentry",
            name="sensor",
            field=models.ForeignKey(to="oversight.Sensor", on_delete=models.CASCADE),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="logentry",
            name="datetime",
            field=models.DateTimeField(
                default=django.utils.timezone.now, db_index=True
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="logentry",
            name="datetime",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name="logentry",
            index_together=set([("sensor", "datetime")]),
        ),
    ]
