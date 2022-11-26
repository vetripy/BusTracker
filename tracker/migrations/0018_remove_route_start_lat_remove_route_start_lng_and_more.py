# Generated by Django 4.1.3 on 2022-11-26 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0017_rename_start_long_route_start_lng'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='start_lat',
        ),
        migrations.RemoveField(
            model_name='route',
            name='start_lng',
        ),
        migrations.AddField(
            model_name='route',
            name='start_stop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='start_stop', to='tracker.stops'),
        ),
    ]
